from typing import List, Optional, Union, Literal, Any

from pydantic import BaseModel


# Video Room API
class CreateRequest(BaseModel):
    # unique ID, optional, chosen by plugin if missing
    room: Optional[Union[int, str]] = None
    # true|false, whether the room should be saved in the config file, default=false
    permanent: Optional[bool] = None
    # pretty name of the room, optional
    description: Optional[str] = None
    # password required to edit/destroy the room, optional
    secret: Optional[str] = None
    # password required to join the room, optional
    pin: Optional[str] = None
    # true|false, whether the room should appear in a list request
    is_private: Optional[bool] = None
    # array of string tokens users can use to join this room, optional
    allowed: Optional[List[str]] = None
    # true|false (whether subscriptions are required to provide a valid private_id to associate with a publisher, default=false)
    require_pvtid: Optional[bool] = None
    # max number of concurrent senders (e.g., 6 for a video conference or 1 for a webinar, default=3)
    publishers: Optional[int] = None
    # max video bitrate for senders> (e.g., 128000)
    bitrate: Optional[int] = None
    # true|false, whether the above cap should act as a limit to dynamic bitrate changes by publishers, default=false
    bitrate_cap: Optional[bool] = None
    # send a FIR to publishers every fir_freq seconds (0=disable)
    fir_freq: Optional[int] = None
    # opus|g722|pcmu|pcma|isac32|isac16 (audio codec to force on publishers, default=opus can be a comma separated list in order of preference, e.g., opus,pcmu)
    audiocodec: Optional[str] = None
    # vp8|vp9|h264|av1|h265 (video codec to force on publishers, default=vp8 can be a comma separated list in order of preference, e.g., vp9,vp8,h264)
    videocodec: Optional[str] = None
    # VP9-specific profile to prefer (e.g., "2" for "profile-id=2")
    vp9_profile: Optional[str] = None
    # H.264-specific profile to prefer (e.g., "42e01f" for "profile-level-id=42e01f")
    h264_profile: Optional[str] = None
    # true|false (whether inband FEC must be negotiated; only works for Opus, default=false)
    opus_fec: Optional[bool] = None
    # true|false (whether SVC support must be enabled; only works for VP9, default=false)
    video_svc: Optional[bool] = None
    # true|false (whether the ssrc-audio-level RTP extension must be negotiated/used or not for new publishers, default=true)
    audiolevel_ext: Optional[bool] = None
    # true|false (whether to emit event to other users or not, default=false)
    audiolevel_event: Optional[bool] = None
    # 100 (number of packets with audio level, default=100, 2 seconds)
    audio_active_packets: Optional[int] = None
    # 25 (average value of audio level, 127=muted, 0='too loud', default=25)
    audio_level_average: Optional[int] = None
    # true|false (whether the video-orientation RTP extension must be negotiated/used or not for new publishers, default=true)
    videoorient_ext: Optional[bool] = None
    # true|false (whether the playout-delay RTP extension must be negotiated/used or not for new publishers, default=true)
    playoutdelay_ext: Optional[bool] = None
    # true|false (whether the transport wide CC RTP extension must be negotiated/used or not for new publishers, default=true)
    transport_wide_cc_ext: Optional[bool] = None
    # true|false (whether this room should be recorded, default=false)
    record: Optional[bool] = None
    # folder where recordings should be stored, when enabled
    rec_dir: Optional[str] = None
    # true|false (whether recording can only be started/stopped if the secret is provided, or using the global enable_recording request, default=false)
    lock_record: Optional[bool] = None
    """
    true|false (optional, whether to notify all participants when a new
    participant joins the room. The Videoroom plugin by design only notifies
    new feeds (publishers), and enabling this may result extra notification
    traffic. This flag is particularly useful when enabled with require_pvtid
    for admin to manage listening only participants. default=false)
    """
    notify_joining: Optional[bool] = None
    # true|false (whether all participants are required to publish and subscribe using end-to-end media encryption, e.g., via Insertable Streams; default=false)
    require_e2ee: Optional[bool] = None
    # request
    request: str = "create"


class EditRequest(BaseModel):
    # unique ID of the room to edit
    room: Optional[Union[int, str]] = None
    # room secret, mandatory if configured
    secret: Optional[str] = None
    # new pretty name of the room, optional
    new_description: Optional[str] = None
    # new password required to edit/destroy the room, optional
    new_secret: Optional[str] = None
    # new password required to join the room, optional
    new_pin: Optional[str] = None
    # true|false, whether the room should appear in a list request
    new_is_private: Optional[bool] = None
    # true|false, whether the room should require private_id from subscribers
    new_require_pvtid: Optional[bool] = None
    # new bitrate cap to force on all publishers (except those with custom overrides)
    new_bitrate: Optional[bool] = None
    # new period for regular PLI keyframe requests to publishers
    new_fir_freq: Optional[bool] = None
    # new cap on the number of concurrent active WebRTC publishers
    new_publishers: Optional[int] = None
    # true|false, whether recording state can only be changed when providing the room secret
    new_lock_record: Optional[bool] = None
    # true|false, whether the room should be also removed from the config file, default=false
    permanent: Optional[bool] = None
    # request
    request: str = "edit"


class DestoryRequest(BaseModel):
    # unique ID of the room to destroy
    room: Union[int, str]
    # room secret, mandatory if configured
    secret: Optional[str] = None
    # true|false, whether the room should be also removed from the config file, default=false
    permanent: Optional[bool] = None
    # request
    request: str = "destory"


class ExistsRequest(BaseModel):
    # unique ID of the room to destroy
    room: Union[int, str]
    # request
    request: str = "exist"


class AllowedRequest(BaseModel):
    # room secret, mandatory if configured
    secret: Optional[str] = None
    # enable|disable|add|remove
    action: Literal["enable", "disable", "add", "remove"]
    # unique ID of the room to update
    room: Union[int, str]
    # Array of strings (tokens users might pass in "join", only for add|remove)
    allowed: Optional[List[str]] = None
    # request
    request: str = "allow"


class KickRequest(BaseModel):
    # room secret, mandatory if configured
    secret: Optional[str] = None
    # unique ID of the room
    room: Union[int, str]
    # unique ID of the participant to kick
    id: Union[int, str]
    # request
    request: str = "kick"


class ModerateRequest(BaseModel):
    # room secret, mandatory if configured
    secret: Optional[str] = None
    # unique ID of the room
    room: Union[int, str]
    # unique ID of the participant to moderate
    id: Union[int, str]
    # mid of the m-line to refer to for this moderate request
    mid: str
    # true|false, depending on whether the media addressed by the above mid should be muted by the moderator
    mute: bool
    # request
    request: str = "moderate"


class ListRequest(BaseModel):
    # request
    request: str = "list"


class ListparticipantsRequest(BaseModel):
    # unique ID of the room
    room: Union[int, str]
    # request
    request: str = "listparticipants"


# VideoRoom Publishers
class PublisherJoinRequest(BaseModel):
    # unique ID of the room
    room: Union[int, str]
    # unique ID to register for the publisher; optional, will be chosen by the plugin if missing
    id: Optional[Union[int, str]] = None
    # display name for the publisher; optional
    display: Optional[str] = None
    # invitation token, in case the room has an ACL; optional
    token: Optional[str] = None
    # participant type
    ptype: str = "publisher"
    # request
    request: str = "join"


class PublishRequest(BaseModel):
    # Should send JSEP SDP
    # <audio codec to prefer among the negotiated ones; optional>
    audiocodec: Optional[str] = None
    # video codec to prefer among the negotiated ones; optional
    videocodec: Optional[str] = None
    # bitrate cap to return via REMB; optional, overrides the global room value if present
    bitrate: Optional[int] = None
    # true|false, whether this publisher should be recorded or not; optional
    record: Optional[bool] = None
    # if recording, the base path/file to use for the recording files; optional
    filename: Optional[str] = None
    # new display name to use in the room; optional
    display: Optional[str] = None
    # if provided, overrided the room audio_level_average for this user; optional
    audio_level_average: Optional[int] = None
    # if provided, overrided the room audio_active_packets for this user; optional
    audio_active_packets: Optional[int] = None
    # Other descriptions, if any
    descriptions: Optional[List[Any]] = None
    # request
    request: str = "publish"


class PublishConfigureRequest(BaseModel):
    # bitrate cap to return via REMB; optional, overrides the global room value if present (unless bitrate_cap is set)
    bitrate: Optional[int] = None
    # true|false, whether we should send this publisher a keyframe request
    keyframe: Optional[bool] = None
    # true|false, whether this publisher should be recorded or not; optional
    record: Optional[bool] = None
    # if recording, the base path/file to use for the recording files; optional
    filename: Optional[str] = None
    # new display name to use in the room; optional
    display: Optional[str] = None
    # if provided, overrided the room audio_level_average for this user; optional
    audio_level_average: Optional[int] = None
    # if provided, overrided the room audio_active_packets for this user; optional
    audio_active_packets: Optional[int] = None
    # mid of the m-line to refer to for this configure request; optional
    mid: Optional[str] = None
    # true|false, depending on whether the media addressed by the above mid should be relayed or not; optional
    send: Optional[bool] = None
    # Updated descriptions for the published streams; see "publish" for syntax; optional
    descriptions: Optional[List[Any]] = None
    # request
    request: str = "configure"


class LeaveRequest(BaseModel):
    # request
    request: str = "leave"


# VideoRoom Subscribers
class Stream(BaseModel):
    # unique ID of publisher owning the stream to subscribe to
    feed_id: Union[int, str]
    # unique mid of the publisher stream to subscribe to; optional
    mid: Optional[str] = None


class SubscriberJoinRequest(BaseModel):
    # unique ID of the room
    room: Union[int, str]
    # unique ID of the publisher to subscribe to; mandatory
    feed: Union[int, str]
    # unique ID of the publisher that originated this request; optional, unless mandated by the room configuration
    private_id: Optional[Union[int, str]] = None
    # Other streams to subscribe to
    streams: Optional[List[Stream]]
    # participant type
    ptype: str = "subscriber"
    # request
    request: str = "join"


class StartRequest(BaseModel):
    # Should send JSEP SDP
    # request
    request: str = "start"


class PauseRequest(BaseModel):
    # request
    request: str = "paused"


class SubscribeRequest(BaseModel):
    # Other streams to subscribe to
    streams: List[Stream]
    # request
    request: str = "subscribe"


class UnsubscribeRequest(BaseModel):
    # Other streams to unsubscribe from
    streams: List[Stream]
    # request
    request: str = "unsubscribe"


class SubscribeConfigureRequest(BaseModel):
    # mid of the m-line to refer to for this configure request; optional
    mid: Optional[str] = None
    # true|false, depending on whether the mindex media should be relayed or not; optional
    send: Optional[bool] = None
    # substream to receive (0-2), in case simulcasting is enabled; optional
    substream: Optional[int] = None
    # temporal layers to receive (0-2), in case simulcasting is enabled; optional
    temporal: Optional[int] = None
    # How much time (in us, default 250000) without receiving packets will make us drop to the substream below
    fallback: Optional[int] = None
    # spatial layer to receive (0-2), in case VP9-SVC is enabled; optional
    spatial_layer: Optional[int] = None
    # temporal layers to receive (0-2), in case VP9-SVC is enabled; optional
    temporal_layer: Optional[int] = None
    # if provided, overrides the room audio_level_average for this user; optional
    audio_level_average: Optional[int] = None
    # if provided, overrides the room audio_active_packets for this user; optional
    audio_active_packets: Optional[int] = None
    # trigger an ICE restart; optional
    restart: Optional[bool] = None
    # request
    request: str = "configure"


class SwitchStream(BaseModel):
    # unique ID of the publisher the new source is from
    feed: Union[int, str]
    # unique mid of the source we want to switch to
    mid: str
    # unique mid of the stream we want to pipe the new source to
    sub_mid: str


class SwitchRequest(BaseModel):
    # streams to switch
    streams: List[SwitchStream]
    # request
    request: str = "switch"
