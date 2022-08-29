from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.types import Date, Integer
from sqlalchemy.orm import relationship
from session import engine1
from session import Base
import datetime


from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData

metadata = MetaData()
# Base = automap_base(bind=engine1, metadata=metadata)


class DocumentModel(Base):
    __table__ = Table('documentmodel', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentType table


class DocumentType(Base):
    __table__ = Table('documenttype', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load Document table


class Document(Base):
    __table__ = Table('document', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load Document table


class DocumentStatus(Base):
    __table__ = Table('documentstatus', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentData table


class DocumentData(Base):
    __table__ = Table('documentdata', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentTagDef table


class DocumentTagDef(Base):
    __table__ = Table('documenttagdef', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentTags table
# class DocumentTags(Base):
#     __table__ = Table('DocumentTags', Base.metadata,
#                           autoload=True, autoload_with=engine1)

# creating class to load DocumentUpdates table


class DocumentUpdates(Base):
    __table__ = Table('documentupdates', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentStage table


class DocumentStage(Base):
    __table__ = Table('documentstage', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentTableDef table


class DocumentTableDef(Base):
    __table__ = Table('documenttabledef', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentLineItems table


class DocumentLineItems(Base):
    __table__ = Table('documentlineitems', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load DocumentLineItemTags table


class DocumentLineItemTags(Base):
    __table__ = Table('documentlineitemtags', Base.metadata,
                      autoload=True, autoload_with=engine1)


class DocumentHistoryLogs(Base):
    __table__ = Table('documenthistorylog', Base.metadata,
                      autoload=True, autoload_with=engine1)

# USER TABLES

# creating class to load customer table


class Customer(Base):
    __table__ = Table('customer', Base.metadata,
                      autoload=True, autoload_with=engine1)

    def datadict(self):
        d = {
            "idCustomer": self.idCustomer,
            "CustomerName": self.CustomerName,
        }
        return d

# creating class to load entitytype table


class EntityType(Base):
    __table__ = Table('entitytype', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load entity table


class Entity(Base):
    __table__ = Table('entity', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load entitybodytype table


class EntityBodyType(Base):
    __table__ = Table('entitybodytype', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load entitybody table


class EntityBody(Base):
    __table__ = Table('entitybody', Base.metadata,
                      autoload=True, autoload_with=engine1)

# creating class to load entitybody table


class Department(Base):
    __table__ = Table('department', Base.metadata,
                      autoload=True, autoload_with=engine1)


class UserAccess(Base):
    """
    stores user access for entity and entity body
    """
    __table__ = Table('useraccess', Base.metadata,
                      autoload=True, autoload_with=engine1)

    def datadict(self):
        d = {
            "idUserAccess": self.idUserAccess,
            "UserID": self.UserID,
            "EntityID": self.EntityID,
            "EntityBodyID": self.EntityBodyID,
            "CreatedBy": self.CreatedBy
        }
        return d


# to store the login table
class Login_info(Base):
    __table__ = Table('login_info_log', Base.metadata,
                      autoload=True, autoload_with=engine1)


# to store the otp and expiry date
class Otp_Code(Base):
    __table__ = Table('password_otp', Base.metadata,
                      autoload=True, autoload_with=engine1)


# creating class to load entitybody table
class User(Base):
    __table__ = Table('user', Base.metadata,
                      autoload=True, autoload_with=engine1)

    def datadict(self):
        d = {
            "idUser": self.idUser,
            "customerID": self.customerID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "contact": self.contact,
            "UserCode": self.UserCode,
            "Designation": self.Designation,
            "email": self.email
        }
        return d


# Vendor Table
class Vendor(Base):
    # __tablename__ = 'Vendor'
    __table__ = Table('vendor', Base.metadata,
                      autoload=True, autoload_with=engine1)


# VendorAccount Table
class VendorAccount(Base):
    # __tablename__ = 'VendorAccount'
    __table__ = Table('vendoraccount', Base.metadata,
                      autoload=True, autoload_with=engine1)


# VendorUserAccess Table
class VendorUserAccess(Base):
    # __tablename__ = 'VendorAccount'
    __table__ = Table('vendoruseraccess', Base.metadata,
                      autoload=True, autoload_with=engine1)


# Vendor Service Table
class ServiceProvider(Base):
    # __tablename__ = 'Service'
    __table__ = Table('serviceprovider', Base.metadata,
                      autoload=True, autoload_with=engine1)


# ServiceAccount Table
class ServiceAccount(Base):
    # __tablename__ = 'ServiceAccount'
    __table__ = Table('serviceaccount', Base.metadata,
                      autoload=True, autoload_with=engine1)


# SupplierSchedule Table
class ServiceProviderSchedule(Base):
    # __tablename__ = 'SupplierSchedule'
    __table__ = Table('serivceproviderschedule', Base.metadata,
                      autoload=True, autoload_with=engine1)


# BatchTriggerHistory Table
class BatchTriggerHistory(Base):
    __table__ = Table('batchprocesshistory', Base.metadata,
                      autoload=True, autoload_with=engine1)


# AccountCostAllocation Table
class AccountCostAllocation(Base):
    # __tablename__ = 'AccountCostAllocation'
    __table__ = Table('accountcostallocation', Base.metadata,
                      autoload=True, autoload_with=engine1)

# Credentials Table


class Credentials(Base):
    # __tablename__ = 'AccountCostAllocation'
    __table__ = Table('credentials', Base.metadata,
                      autoload=True, autoload_with=engine1)
# Preparing the classes to reflect the existing table structure
# Base.prepare(engine1, reflect=True)
# Permisiions


class AccessPermission(Base):
    """
    holds access permission details of the user and vendor
    """
    # __tablename__ = 'accesspermission'
    __table__ = Table('accesspermission', Base.metadata,
                      autoload=True, autoload_with=engine1)

    def datadict(self):
        """
        custom dictionary function to return only required columns
        :return: dictionary of selected columns
        """
        d = {
            "idAccessPermission": self.idAccessPermission,
            "permissionDefID": self.permissionDefID,
            "userID": self.userID,
            "vendorUserID": self.vendorUserID,
            "approvalLevel": self.approvalLevel
        }
        return d


# idAccessPermissionDef Table
class AccessPermissionDef(Base):
    """
    stores the definition of the permission and permission id
    """
    # __tablename__ = 'accesspermissiondef'
    __table__ = Table('accesspermissiondef', Base.metadata,
                      autoload=True, autoload_with=engine1)

    def datadict(self):
        """
        custom dictionary function to return only required columns
        :return: dictionary of selected columns
        """
        d = {
            "idAccessPermissionDef": self.idAccessPermissionDef,
            "NameOfRole": self.NameOfRole,
            "Priority": self.Priority,
            "User": self.User,
            "Permissions": self.Permissions,
            "AccessPermissionTypeId": self.AccessPermissionTypeId,
            "NewInvoice": self.NewInvoice,
            "amountApprovalID": self.amountApprovalID
        }
        return d


# AccessPermissionType Table
class AccessPermissionType(Base):
    # __tablename__ = 'accesspermissiontype'
    __table__ = Table('accesspermissiontype', Base.metadata,
                      autoload=True, autoload_with=engine1)


# AmountApproveLevel Table
class AmountApproveLevel(Base):
    # __tablename__ = 'amountapprovelevel'
    __table__ = Table('amountapprovelevel', Base.metadata,
                      autoload=True, autoload_with=engine1)

    def datadict(self):
        d = {
            "idAmountApproveLevel": self.idAmountApproveLevel,
            "MaxAmount": self.MaxAmount
        }
        return d


#
class ColumnPosDef(Base):
    # __tablename__ = 'amountapprovelevel'
    __table__ = Table('columnnamesdef', Base.metadata,
                      autoload=True, autoload_with=engine1)


class DocumentColumnPos(Base):
    # __tablename__ = 'amountapprovelevel'
    __table__ = Table('documentcolumns', Base.metadata,
                      autoload=True, autoload_with=engine1)


# ----------- FR Tables ------------------

# FR configuration Table


class FRConfiguration(Base):
    __table__ = Table('frconfigurations', Base.metadata,
                      autoload=True, autoload_with=engine1)

# FR Meta Data Table


class FRMetaData(Base):
    __table__ = Table('frmetadata', Base.metadata,
                      autoload=True, autoload_with=engine1)
# OCR Log Table


class OCRLogs(Base):
    __table__ = Table('ocrlogs', Base.metadata,
                      autoload=True, autoload_with=engine1)

# OCR UserItem Mapping


class UserItemMapping(Base):
    __table__ = Table('useritemmapping', Base.metadata,
                      autoload=True, autoload_with=engine1)


# Application General config

class GeneralConfig(Base):
    __table__ = Table('generalconfig', Base.metadata,
                      autoload=True, autoload_with=engine1)



# documentRules data


class Rule(Base):
    __table__ = Table('documentrules', Base.metadata,
                      autoload=True, autoload_with=engine1)

class AGIRule(Base):
    __table__ = Table('erprulecodes', Base.metadata,
                      autoload=True, autoload_with=engine1)


class DocumentSubStatus(Base):
    __table__ = Table('documentsubstatus', Base.metadata,
                      autoload=True, autoload_with=engine1)



class DocumentRulemapping(Base):
    __table__ = Table('docrulestatusmapping', Base.metadata,
                      autoload=True, autoload_with=engine1)

class DocumentRuleupdates(Base):
    __table__ = Table('documentruleshistorylog', Base.metadata,
                      autoload=True, autoload_with=engine1)

class DocumentModelComposed(Base):
    __table__ = Table('documentmodelcomposed', Base.metadata,
                      autoload=True, autoload_with=engine1)


# notification Models

class PullNotification(Base):
    __table__ = Table('pullnotification', Base.metadata,
                      autoload=True, autoload_with=engine1)


class PullNotificationTemplate(Base):
    __table__ = Table('pullnotificationtemplate', Base.metadata,
                      autoload=True, autoload_with=engine1)


class NotificationCategoryRecipient(Base):
    __table__ = Table('notificationrecipents', Base.metadata,
                      autoload=True, autoload_with=engine1)


class TriggerDescription(Base):
    __table__ = Table('triggerdescription', Base.metadata,
                          autoload=True, autoload_with=engine1)


class BatchErrorType(Base):
    __table__ = Table('batcherrortypes', Base.metadata,
                      autoload=True, autoload_with=engine1)


class ItemMetaData(Base):
    __table__ = Table('itemmetadata', Base.metadata,
                      autoload=True, autoload_with=engine1)


class ItemUserMap(Base):
    __table__ = Table('itemusermap', Base.metadata,
                      autoload=True, autoload_with=engine1)

class DefaultFields(Base):
    __table__ = Table('defaultfields', Base.metadata,
                      autoload=True, autoload_with=engine1)


class AgiCostAlloc(Base):
    __table__ = Table('agicostallocation', Base.metadata,
                      autoload=True, autoload_with=engine1)

