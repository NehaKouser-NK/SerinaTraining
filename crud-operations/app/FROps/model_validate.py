import cv2
import numpy as np
from pdf2image import convert_from_path,convert_from_bytes
from azure.storage.blob import BlobClient, BlobServiceClient
import time
import json
import tempfile
import os
from ast import literal_eval

'''req_fields_accuracy = 99.2
req_model_accuracy = 99.5
mand_fld_list = ['customer_no', 'invoice_no']
model_path = 'model-6be0c8c5-882f-4900-b0d9-041c60e3ef22.json'
'''


def model_validate(model_path,fr_modelid,req_fields_accuracy, req_model_accuracy, mand_fld_list):
    model_validate_status = 0
    model_validate_msg = ''
    trin_doc_path = ""
    model_id = ''
    try:
        data = model_path

        tag_list = []

        field_acc_status = 1
        if data['modelInfo']['attributes']['isComposed'] == True:
            key = 'composedTrainResults'
            index = next((index for (index, d) in enumerate(data[key]) if d["modelId"] == fr_modelid), None)
            if index is None:
                index = 0
            model_accuracy = data[key][index]['averageModelAccuracy']
            model_id = data["modelInfo"]["modelId"]
            trin_doc_path = data[key][index]['trainingDocuments'][0]['documentName']
            for fld in data[key][index]['fields']:
                tag_list.append(fld['fieldName'])

                # check for field accuracy:
                if ((fld['accuracy']) * 100) >= req_fields_accuracy:
                    field_acc_status = field_acc_status * 1
                else:
                    field_acc_status = field_acc_status * 0
                    print(fld['fieldName'], fld['accuracy'])
        else:
            key = 'trainResult'
            model_accuracy = data[key]['averageModelAccuracy']
            model_id = data["modelInfo"]["modelId"]
            trin_doc_path = data[key]['trainingDocuments'][0]['documentName']
            for fld in data[key]['fields']:
                tag_list.append(fld['fieldName'])

                # check for field accuracy:
                if ((fld['accuracy']) * 100) >= req_fields_accuracy:
                    field_acc_status = field_acc_status * 1
                else:
                    field_acc_status = field_acc_status * 0
                    print(fld['fieldName'], fld['accuracy'])
        if (model_accuracy) * 100 >= req_model_accuracy:
            model_accuracy_status = 1
        else:
            model_accuracy_status = 0
            model_validate_msg = model_validate_msg + \
                "| Model overall accuracy not satisfied |"
        if field_acc_status == 0:
            model_validate_msg = model_validate_msg + \
                "|Model field accuracy not satisfied|"

        # check for mandatory:
        if set(mand_fld_list).issubset(set(tag_list)) == True:
            mand_fld_list_status = 1
        else:
            mand_fld_list_status = 0
            model_validate_msg = model_validate_msg + \
                "|Mandatory field missing while tagging|"
        if model_accuracy_status == field_acc_status == mand_fld_list_status == 1:
            model_validate_status = 1
            model_validate_msg = "Model accepted"
        else:
            model_validate_status = 0
            # model_validate_msg = "Model is rejected"

    except Exception as e:
        trin_doc_path = ""
        model_validate_msg = str(e)
        model_validate_status = 0
    return model_validate_status, model_validate_msg, model_id, trin_doc_path


cnt_str = "DefaultEndpointsProtocol=https;AccountName=testblob0203;AccountKey=h3ro+ZcNm1Y7F2GZz1ESrRbz6kiu5PBKTAmK2iB+KNdlnw8ZaAycjjwrsvO6drtBQHYMR/NlwdOBi1BJKojJLg==;EndpointSuffix=core.windows.net"  # connection string
cnt_nm = "upload1"
VendorAccount = "123"
ServiceAccount = "456"
model_id = "456789"
old_fld_name = '1623148701_5608163'
template_metadata = {}


def db_push_data(cnt_str, cnt_nm, VendorAccount, ServiceAccount, model_id, trin_doc_path, template_metadata):
    data_mdy = {}
    db_push_status = "Issue with .label file"
    db_push_msg = 0
    old_fld_name = trin_doc_path.split("/")[0]
    temp_dir = "tempdir/train_docs"
    file_path = temp_dir+"/"+old_fld_name + '.json'
    try:

        blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=cnt_str, container_name=cnt_nm)
        container_client = blob_service_client.get_container_client(cnt_nm)
        print("train doc path", trin_doc_path)
        blb_file_nm = trin_doc_path.rsplit(".",1)[0]
        print("blob file name", blb_file_nm)
        pdf_blb_pth = blb_file_nm + ".pdf"
        label_blb_pth = blb_file_nm + ".pdf.labels.json"

        blob_service_client = BlobServiceClient.from_connection_string(cnt_str)
        blb_container = blob_service_client.get_container_client(cnt_nm)
        # get pdf:
        pdf_byts = blb_container.get_blob_client(
            pdf_blb_pth).download_blob().readall()
        lbl_byts = blb_container.get_blob_client(
            label_blb_pth).download_blob().readall()

        #container_client.upload_blob(name=temp_dir+"/"+old_fld_name + ".pdf", data=pdf_byts)
        # with open(temp_dir+"/"+old_fld_name + ".pdf", "wb") as f:
        #     f.write(pdf_byts)
        #     f.close()
        #container_client.upload_blob(name=temp_dir+"/"+old_fld_name + ".pdf.labels.json", data=lbl_byts)
        # with open(old_fld_name + ".pdf.labels.json", "wb") as f:
        #     f.write(lbl_byts)
        #     f.close()

        # with open(old_fld_name + '.pdf.labels.json', encoding='utf-8') as f:
        #     data = json.load(f)
        #     f.close()
        data = json.loads(lbl_byts)
        img = convert_from_bytes(pdf_byts,poppler_path=r'/usr/bin')
        # img = convert_from_bytes(pdf_byts,poppler_path=r'D:\\poppler-0.68.0\\bin')
        mlt_ig = 1
        for ig in img:
            image = np.array(ig)
        image.shape
        xi = image.shape[0]
        yi = image.shape[1]
        if VendorAccount is not None:
            data['VendorAccount'] = VendorAccount
        if ServiceAccount is not None:
            data['ServiceAccount'] = ServiceAccount
        data['ModelID'] = model_id
        for nn in data['labels']:
            if nn['key'] is None:
                nn['key'] = ''

        for i in data['labels']:
            for j in i['value']:
                ct = 0
                bo_bx = []
                bx = {}
                for k in j['boundingBoxes'][0]:
                    if ct == 0:
                        tmp_x = float(k) * xi
                        bo_bx.append(tmp_x)
                        ct = 1
                    elif ct == 1:
                        tmp_y = float(k) * yi
                        ct = 0
                        bo_bx.append(tmp_y)

                x = str(bo_bx[0])
                y = str(bo_bx[1])
                w = str(bo_bx[2] - bo_bx[0])
                h = str(bo_bx[5] - bo_bx[1])
                bx['x'] = x
                bx['y'] = y
                bx['w'] = w
                bx['h'] = h
                j['boundingBoxes'] = bx
                # print(data.keys())
        data_mdy = data
        data_mdy['Schema'] = data_mdy['$schema']
        del data_mdy['$schema']

        # -------------------

        data_mdy['other_tables'] = {}
        data_mdy['line_tables'] = {}
        data_mdy['new_labels'] = []

        tmp_lbl = []

        for lbl in data_mdy['labels']:
            # print(lbl['label'])
            if str(lbl['label']).split("/")[0][0:3] == 'tab':
                tmp_lbl.append(str(lbl['label']).split("/")[0])
        tmp_lbl
        lbl_set = set(tmp_lbl)

        for uq_tbl in lbl_set:
            data_mdy['line_tables'][uq_tbl] = []
        ck_tab = 0
        for lbl in data_mdy['labels']:
            if str(lbl['label']).split("/")[0][0:3] == 'tab':
                ck_tab = 1
                dt = {'col': str(lbl['label']).split("/")[2], 'row': str(lbl['label']).split("/")[1],
                      "value": lbl['value']}
                data_mdy['line_tables'][str(
                    lbl['label']).split("/")[0]].append(dt)
            else:
                data_mdy['new_labels'].append(lbl)
        del data_mdy['labels']
        data_mdy['labels'] = data_mdy['new_labels']
        del data_mdy['new_labels']
        if ck_tab == 1:
            if 'tab_1' in data_mdy['line_tables']:
                for cl_rc in range(len(data_mdy['line_tables']['tab_1'])):
                    if data_mdy['line_tables']['tab_1'][cl_rc]['row'] == '0':
                        x_vl = []
                        y_vl = []
                        for vlbx in data_mdy['line_tables']['tab_1'][cl_rc]['value']:
                            x_vl.append(float(vlbx['boundingBoxes']['x']))
                            x_vl.append(
                                float(vlbx['boundingBoxes']['x']) + float(vlbx['boundingBoxes']['w']))
                            y_vl.append(float(vlbx['boundingBoxes']['y']))
                            y_vl.append(
                                float(vlbx['boundingBoxes']['y']) + float(vlbx['boundingBoxes']['h']))
                        nw_val = {
                            'page': 1, 'text': data_mdy['line_tables']['tab_1'][cl_rc]['col']}
                        h = str(max(y_vl,default=0) - min(y_vl,default=0))
                        w = str(max(x_vl,default=0) - min(x_vl,default=0))
                        x = str(min(x_vl,default=0))
                        y = str(min(y_vl,default=0))
                        nw_val['boundingBoxes'] = {
                            'x': x, 'y': y, 'w': w, 'h': h}
                        del data_mdy['line_tables']['tab_1'][cl_rc]['value']
                        data_mdy['line_tables']['tab_1'][cl_rc]['value'] = [
                            nw_val]
            else:
                db_push_msg = "tab_1 is missing"
                db_push_status = 0

        # ------------------

        if 'VendorAccount' in data.keys():
            data_mdy['template_metadata'] = template_metadata
            container_client.upload_blob(name=file_path, data=json.dumps(data_mdy),overwrite=True)
            # print(data_mdy.keys())
            db_push_status = 1
            db_push_msg = "Created " + str(old_fld_name) + ".json"
        
        elif 'ServiceAccount' in data.keys():
            data_mdy['template_metadata'] = template_metadata
            container_client.upload_blob(name=file_path, data=json.dumps(data_mdy),overwrite=True)
            # print(data_mdy.keys())
            db_push_status = 1
            db_push_msg = "Created " + str(old_fld_name) + ".json"

        else:
            db_push_status = 0
            db_push_msg = "Issue with Model merge!"
    except Exception as e:
        db_push_status = 0
        db_push_msg = "db push error: "+str(e)
    return db_push_status, db_push_msg, file_path, data_mdy


def model_validate_final(model_path,fr_modelid,req_fields_accuracy, req_model_accuracy, mand_fld_list, cnt_str, cnt_nm, VendorAccount, ServiceAccount, template_metadata):
    model_id = ''
    file_path = ''
    data = {}
    try:
        model_validate_status, model_validate_msg, model_id, trin_doc_path = model_validate(
            model_path,fr_modelid,req_fields_accuracy, req_model_accuracy, mand_fld_list)
        print("model_validate_status ", model_validate_status,
              " model_validate_msg", model_validate_msg)
        if model_validate_status == 1:
            db_push_status, db_push_msg, file_path, data = db_push_data(
                cnt_str, cnt_nm, VendorAccount, ServiceAccount, model_id, trin_doc_path, template_metadata)
            if db_push_status == 1:
                model_validate_final_status = 1
                model_validate_final_msg = "Model Accepted and DB push data created"
            else:
                model_validate_final_status = 0
                model_validate_final_msg = db_push_msg
        else:
            model_validate_final_status = 0
            model_validate_final_msg = model_validate_msg

    except Exception as e:
        model_validate_final_status = 0
        model_validate_final_msg = "Error: "+str(e)
    return model_validate_final_status, model_validate_final_msg, model_id, file_path, data
