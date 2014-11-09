from zlib import crc32
import struct

_NAMES = {}

_PYTHON_SUGAR = {}

def pack(data):
    """Utility function to pack a 32 bit integer"""
    return struct.pack("I", data)

def tl_get_type_name(t):
    """Utility function to get the type name of a type"""
    if t == int:
        return "int"
    else:
        return t.NAME

def tl_get_arguments(args):
    result = []

    while args:
        name, t, *args = args
        result.append("{}:{}".format(name, tl_get_type_name(t)))

    return " ".join(result) + " " if result else ""

def tl_encode(self):
    """Encode any value to the TL binary format"""
    if self in _PYTHON_SUGAR:
        return tl_encode(_PYTHON_SUGAR[self])
    elif isinstance(self, int):
        return pack(self)
    else:
        result = type(self).ID
        args = type(self).ARGS

        while args:
            name, t, *args = args
            result += tl_encode(getattr(self, name))
        return result


def tl_type(name, return_type, *args):
    """Decorator to turn a python type into an encodable TL type"""
    def decorator(klass):
        klass.NAME = name
        tl_name = "{name} {arguments}= {return_type}".format(
            name=name, 
            return_type=tl_get_type_name(return_type), 
            arguments=tl_get_arguments(args))
        klass.TL_NAME = tl_name
        klass.ID = pack(crc32(tl_name.encode("ascii")) % 2**32)
        klass.ARGS = args
        klass.encode = tl_encode
        return klass
    return decorator

def sugar(value):
    """Decorator to define a python value to be sugar for a singleton of this class."""
    def decorator(klass):
        _PYTHON_SUGAR[value] = klass()
        return klass
    return decorator

# Primary Types

class Bool:
    NAME = "Bool"

class Null:
    NAME = "Null"

# Primary Type Instances

class Long:
    NAME = "long"

    def __init__(self, value):
        self.value = value

    def encode(self):
        return struct.pack("L", self.value)

@tl_type("boolFalse", Bool)
@sugar(False)
class BoolFalse:
    pass

@tl_type("boolTrue", Bool)
@sugar(True)
class BoolTrue:
    pass

@tl_type("null", Null)
@sugar(None)
class Null:
    pass

# Types

class InputPeer:
    NAME = "InputPeer"

class InputUser:
    NAME = "InputUser"

# Instances

@tl_type("inputPeerEmpty", InputPeer)
class InputPeerEmpty:
    pass

@tl_type("inputPeerSelf", InputPeer)
class InputPeerSelf:
    pass

@tl_type("inputPeerContact", InputPeer, "user_id", int)
class InputPeerContact:
    def __init__(self, user_id):
        self.user_id = user_id

@tl_type("inputPeerForeign", InputPeer, "user_id", int, "access_hash", Long)
class InputPeerForeign:
    def __init__(self, user_id, access_hash):
        self.user_id = user_id
        self.access_hash = access_hash

@tl_type("inputUserEmpty", InputUser)
class InputUserEmpty:
    pass

@tl_type("inputUserSelf", InputUser)
class InputUserSelf:
    pass

@tl_type("inputUserContact", InputUser, "user_id", int)
class InputUserContact:
    def __init__(self, user_id):
        self.user_id = user_id

@tl_type("inputUserForeign", InputUser, "user_id", int, "access_hash", Long)
class InputUserForeign:
    def __init__(self, user_id, access_hash):
        self.user_id = user_id
        self.access_hash = access_hash

# inputPhoneContact client_id:long phone:string first_name:string last_name:string = InputContact;

# inputFile id:long parts:int name:string md5_checksum:string = InputFile;

# inputMediaEmpty = InputMedia;
# inputMediaUploadedPhoto file:InputFile = InputMedia;
# inputMediaPhoto id:InputPhoto = InputMedia;
# inputMediaGeoPoint geo_point:InputGeoPoint = InputMedia;
# inputMediaContact phone_number:string first_name:string last_name:string = InputMedia;
# inputMediaUploadedVideo file:InputFile duration:int w:int h:int mime_type:string = InputMedia;
# inputMediaUploadedThumbVideo file:InputFile thumb:InputFile duration:int w:int h:int mime_type:string = InputMedia;
# inputMediaVideo id:InputVideo = InputMedia;

# inputChatPhotoEmpty = InputChatPhoto;
# inputChatUploadedPhoto file:InputFile crop:InputPhotoCrop = InputChatPhoto;
# inputChatPhoto id:InputPhoto crop:InputPhotoCrop = InputChatPhoto;

# inputGeoPointEmpty = InputGeoPoint;
# inputGeoPoint lat:double long:double = InputGeoPoint;

# inputPhotoEmpty = InputPhoto;
# inputPhoto id:long access_hash:long = InputPhoto;

# inputVideoEmpty = InputVideo;
# inputVideo id:long access_hash:long = InputVideo;

# inputFileLocation volume_id:long local_id:int secret:long = InputFileLocation;
# inputVideoFileLocation id:long access_hash:long = InputFileLocation;

# inputPhotoCropAuto = InputPhotoCrop;
# inputPhotoCrop crop_left:double crop_top:double crop_width:double = InputPhotoCrop;

# inputAppEvent time:double type:string peer:long data:string = InputAppEvent;

# peerUser user_id:int = Peer;
# peerChat chat_id:int = Peer;

# storage.fileUnknown = storage.FileType;
# storage.fileJpeg#7efe0e = storage.FileType;
# storage.fileGif = storage.FileType;
# storage.filePng#a4f63c0 = storage.FileType;
# storage.filePdf = storage.FileType;
# storage.fileMp3 = storage.FileType;
# storage.fileMov = storage.FileType;
# storage.filePartial = storage.FileType;
# storage.fileMp4 = storage.FileType;
# storage.fileWebp = storage.FileType;

# fileLocationUnavailable volume_id:long local_id:int secret:long = FileLocation;
# fileLocation dc_id:int volume_id:long local_id:int secret:long = FileLocation;

# userEmpty id:int = User;
# userSelf id:int first_name:string last_name:string username:string phone:string photo:UserProfilePhoto status:UserStatus inactive:Bool = User;
# userContact id:int first_name:string last_name:string username:string access_hash:long phone:string photo:UserProfilePhoto status:UserStatus = User;
# userRequest id:int first_name:string last_name:string username:string access_hash:long phone:string photo:UserProfilePhoto status:UserStatus = User;
# userForeign#75cf7a8 id:int first_name:string last_name:string username:string access_hash:long photo:UserProfilePhoto status:UserStatus = User;
# userDeleted id:int first_name:string last_name:string username:string = User;

# userProfilePhotoEmpty = UserProfilePhoto;
# userProfilePhoto photo_id:long photo_small:FileLocation photo_big:FileLocation = UserProfilePhoto;

# userStatusEmpty#9d05049 = UserStatus;
# userStatusOnline expires:int = UserStatus;
# userStatusOffline#8c703f was_online:int = UserStatus;

# chatEmpty id:int = Chat;
# chat id:int title:string photo:ChatPhoto participants_count:int date:int left:Bool version:int = Chat;
# chatForbidden id:int title:string date:int = Chat;

# chatFull id:int participants:ChatParticipants chat_photo:Photo notify_settings:PeerNotifySettings = ChatFull;

# chatParticipant user_id:int inviter_id:int date:int = ChatParticipant;

# chatParticipantsForbidden#fd2bb8a chat_id:int = ChatParticipants;
# chatParticipants chat_id:int admin_id:int participants:Vector<ChatParticipant> version:int = ChatParticipants;

# chatPhotoEmpty = ChatPhoto;
# chatPhoto photo_small:FileLocation photo_big:FileLocation = ChatPhoto;

# messageEmpty id:int = Message;
# message flags:int id:int from_id:int to_id:Peer date:int message:string media:MessageMedia = Message;
# messageForwarded flags:int id:int fwd_from_id:int fwd_date:int from_id:int to_id:Peer date:int message:string media:MessageMedia = Message;
# messageService flags:int id:int from_id:int to_id:Peer date:int action:MessageAction = Message;

# messageMediaEmpty = MessageMedia;
# messageMediaPhoto photo:Photo = MessageMedia;
# messageMediaVideo video:Video = MessageMedia;
# messageMediaGeo geo:GeoPoint = MessageMedia;
# messageMediaContact phone_number:string first_name:string last_name:string user_id:int = MessageMedia;
# messageMediaUnsupported bytes:bytes = MessageMedia;

# messageActionEmpty = MessageAction;
# messageActionChatCreate title:string users:Vector<int> = MessageAction;
# messageActionChatEditTitle title:string = MessageAction;
# messageActionChatEditPhoto photo:Photo = MessageAction;
# messageActionChatDeletePhoto = MessageAction;
# messageActionChatAddUser user_id:int = MessageAction;
# messageActionChatDeleteUser user_id:int = MessageAction;

# dialog peer:Peer top_message:int unread_count:int notify_settings:PeerNotifySettings = Dialog;

# photoEmpty id:long = Photo;
# photo id:long access_hash:long user_id:int date:int caption:string geo:GeoPoint sizes:Vector<PhotoSize> = Photo;

# photoSizeEmpty#e17e23c type:string = PhotoSize;
# photoSize type:string location:FileLocation w:int h:int size:int = PhotoSize;
# photoCachedSize type:string location:FileLocation w:int h:int bytes:bytes = PhotoSize;

# videoEmpty id:long = Video;
# video id:long access_hash:long user_id:int date:int caption:string duration:int mime_type:string size:int thumb:PhotoSize dc_id:int w:int h:int = Video;

# geoPointEmpty = GeoPoint;
# geoPoint long:double lat:double = GeoPoint;

# auth.checkedPhone phone_registered:Bool phone_invited:Bool = auth.CheckedPhone;

# auth.sentCode phone_registered:Bool phone_code_hash:string send_call_timeout:int is_password:Bool = auth.SentCode;

# auth.authorization expires:int user:User = auth.Authorization;

# auth.exportedAuthorization id:int bytes:bytes = auth.ExportedAuthorization;

# inputNotifyPeer peer:InputPeer = InputNotifyPeer;
# inputNotifyUsers = InputNotifyPeer;
# inputNotifyChats = InputNotifyPeer;
# inputNotifyAll = InputNotifyPeer;

# inputPeerNotifyEventsEmpty = InputPeerNotifyEvents;
# inputPeerNotifyEventsAll = InputPeerNotifyEvents;

# inputPeerNotifySettings mute_until:int sound:string show_previews:Bool events_mask:int = InputPeerNotifySettings;

# peerNotifyEventsEmpty = PeerNotifyEvents;
# peerNotifyEventsAll = PeerNotifyEvents;

# peerNotifySettingsEmpty = PeerNotifySettings;
# peerNotifySettings mute_until:int sound:string show_previews:Bool events_mask:int = PeerNotifySettings;

# wallPaper id:int title:string sizes:Vector<PhotoSize> color:int = WallPaper;

# userFull user:User link:contacts.Link profile_photo:Photo notify_settings:PeerNotifySettings blocked:Bool real_first_name:string real_last_name:string = UserFull;

# contact user_id:int mutual:Bool = Contact;

# importedContact user_id:int client_id:long = ImportedContact;

# contactBlocked user_id:int date:int = ContactBlocked;

# contactSuggested user_id:int mutual_contacts:int = ContactSuggested;

# contactStatus user_id:int expires:int = ContactStatus;

# chatLocated chat_id:int distance:int = ChatLocated;

# contacts.foreignLinkUnknown = contacts.ForeignLink;
# contacts.foreignLinkRequested has_phone:Bool = contacts.ForeignLink;
# contacts.foreignLinkMutual = contacts.ForeignLink;

# contacts.myLinkEmpty = contacts.MyLink;
# contacts.myLinkRequested contact:Bool = contacts.MyLink;
# contacts.myLinkContact = contacts.MyLink;

# contacts.link my_link:contacts.MyLink foreign_link:contacts.ForeignLink user:User = contacts.Link;

# contacts.contacts contacts:Vector<Contact> users:Vector<User> = contacts.Contacts;
# contacts.contactsNotModified = contacts.Contacts;

# contacts.importedContacts imported:Vector<ImportedContact> retry_contacts:Vector<long> users:Vector<User> = contacts.ImportedContacts;

# contacts.blocked blocked:Vector<ContactBlocked> users:Vector<User> = contacts.Blocked;
# contacts.blockedSlice count:int blocked:Vector<ContactBlocked> users:Vector<User> = contacts.Blocked;

# contacts.suggested results:Vector<ContactSuggested> users:Vector<User> = contacts.Suggested;

# messages.dialogs dialogs:Vector<Dialog> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Dialogs;
# messages.dialogsSlice count:int dialogs:Vector<Dialog> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Dialogs;

# messages.messages messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Messages;
# messages.messagesSlice#b446ae3 count:int messages:Vector<Message> chats:Vector<Chat> users:Vector<User> = messages.Messages;

# messages.messageEmpty = messages.Message;
# messages.message message:Message chats:Vector<Chat> users:Vector<User> = messages.Message;

# messages.statedMessages messages:Vector<Message> chats:Vector<Chat> users:Vector<User> pts:int seq:int = messages.StatedMessages;

# messages.statedMessage message:Message chats:Vector<Chat> users:Vector<User> pts:int seq:int = messages.StatedMessage;

# messages.sentMessage id:int date:int pts:int seq:int = messages.SentMessage;

# messages.chat chat:Chat users:Vector<User> = messages.Chat;

# messages.chats chats:Vector<Chat> users:Vector<User> = messages.Chats;

# messages.chatFull full_chat:ChatFull chats:Vector<Chat> users:Vector<User> = messages.ChatFull;

# messages.affectedHistory pts:int seq:int offset:int = messages.AffectedHistory;

# inputMessagesFilterEmpty = MessagesFilter;
# inputMessagesFilterPhotos = MessagesFilter;
# inputMessagesFilterVideo = MessagesFilter;
# inputMessagesFilterPhotoVideo = MessagesFilter;
# inputMessagesFilterDocument = MessagesFilter;
# inputMessagesFilterAudio = MessagesFilter;


# Methods

