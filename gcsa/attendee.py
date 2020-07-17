class ResponseStatus:
    """Possible values for attendee's response status

    * NEEDS_ACTION - The attendee has not responded to the invitation.
    * DECLINED - The attendee has declined the invitation.
    * TENTATIVE - The attendee has tentatively accepted the invitation.
    * ACCEPTED - The attendee has accepted the invitation.
    """
    NEEDS_ACTION = "needsAction"
    DECLINED = "declined"
    TENTATIVE = "tentative"
    ACCEPTED = "accepted"


class Attendee:
    def __init__(self,
                 email,
                 display_name=None,
                 comment=None,
                 optional=None,
                 is_resource=None,
                 additional_guests=None,
                 response_status=None):
        """Represents attendee of the event.

        :param email:
                the attendee's email address, if available.
        :param display_name:
                the attendee's name, if available
        :param comment:
                the attendee's response comment
        :param optional:
                whether this is an optional attendee. The default is False.
        :param is_resource:
                whether the attendee is a resource.
                Can only be set when the attendee is added to the event
                for the first time. Subsequent modifications are ignored.
                The default is False.
        :param additional_guests:
                number of additional guests. The default is 0.
        :param response_status:
                the attendee's response status. See :py:class:`~gcsa.attendee.ResponseStatus`
        """
        self.email = email
        self.display_name = display_name
        self.comment = comment
        self.optional = optional
        self.is_resource = is_resource
        self.additional_guests = additional_guests
        self.response_status = response_status
