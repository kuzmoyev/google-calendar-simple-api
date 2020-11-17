from uuid import uuid4


class SolutionType:
    """
        * HANGOUT - for Hangouts for consumers (hangouts.google.com)
        * NAMED_HANGOUT - for classic Hangouts for Google Workspace users (hangouts.google.com)
        * HANGOUTS_MEET - for Google Meet (meet.google.com)
        * ADD_ON - for 3P conference providers
    """

    HANGOUT = 'eventHangout'
    NAMED_HANGOUT = 'eventNamedHangout'
    HANGOUTS_MEET = 'hangoutsMeet'
    ADD_ON = 'addOn'


class _BaseConferenceSolution:
    """General conference-related information."""

    def __init__(
            self,
            conference_id=None,
            signature=None,
            notes=None
    ):
        """
        :param conference_id:
                The ID of the conference. Optional.
                Can be used by developers to keep track of conferences, should not be displayed to users.

                Values for solution types (see :py:class:`~gcsa.conference.SolutionType`):

                * HANGOUT: unset
                * NAMED_HANGOUT: the name of the Hangout
                * HANGOUTS_MEET: the 10-letter meeting code, for example "aaa-bbbb-ccc"
                * ADD_ON: defined by 3P conference provider

        :param signature:
                The signature of the conference data.
                Generated on server side. Must be preserved while copying the conference data between events,
                otherwise the conference data will not be copied.
                None for a conference with a failed create request.
                Optional for a conference with a pending create request.
        :param notes:
                String of additional notes (such as instructions from the domain administrator, legal notices)
                to display to the user. Can contain HTML. The maximum length is 2048 characters
        """
        if notes and len(notes) > 2048:
            raise ValueError('Maximum notes length is 2048 characters.')

        self.conference_id = conference_id
        self.signature = signature
        self.notes = notes


class EntryPoint:
    """Information about individual conference entry points, such as URLs or phone numbers."""

    def __init__(
            self,
            entry_point_type=None,
            uri=None,
            label=None,
            pin=None,
            access_code=None,
            meeting_code=None,
            passcode=None,
            password=None
    ):
        """
        When creating new conference data, populate only the subset of `meeting_code`, `access_code`, `passcode`,
        `password`, and `pin` fields that match the terminology that the conference provider uses.

        Only the populated fields should be displayed.

        :param entry_point_type:
                The type of the conference entry point.

                Possible values are:

                * | "video" - joining a conference over HTTP.
                  | A conference can have zero or one "video" entry point.
                * | "phone" - joining a conference by dialing a phone number.
                  | A conference can have zero or more "phone" entry points.
                * | "sip" - joining a conference over SIP.
                  | A conference can have zero or one "sip" entry point.
                * | "more" - further conference joining instructions, for example additional phone numbers.
                  | A conference can have zero or one "more" entry point.
                  | A conference with only a "more" entry point is not a valid conference.

        :param uri:
                The URI of the entry point. The maximum length is 1300 characters.
                Format:

                * | for "video", http: or https: schema is required.
                * | for "phone", tel: schema is required.
                  | The URI should include the entire dial sequence (e.g., tel:+12345678900,,,123456789;1234).
                * | for "sip", sip: schema is required, e.g., sip:12345678@myprovider.com.
                * | for "more", http: or https: schema is required.

        :param label:
                The label for the URI.
                Visible to end users. Not localized. The maximum length is 512 characters.

                Examples:

                * for "video": meet.google.com/aaa-bbbb-ccc
                * for "phone": +1 123 268 2601
                * for "sip": 12345678@altostrat.com
                * for "more": should not be filled

        :param pin:
                The PIN to access the conference. The maximum length is 128 characters.
        :param access_code:
                The access code to access the conference. The maximum length is 128 characters. Optional.
        :param meeting_code:
                The meeting code to access the conference. The maximum length is 128 characters.
        :param passcode:
                The passcode to access the conference. The maximum length is 128 characters.
        :param password:
                The password to access the conference. The maximum length is 128 characters.
        """
        if label and len(label) > 512:
            raise ValueError('Maximum label length is 512 characters.')
        if pin and len(pin) > 128:
            raise ValueError('Maximum pin length is 128 characters.')
        if access_code and len(access_code) > 128:
            raise ValueError('Maximum access_code length is 128 characters.')
        if meeting_code and len(meeting_code) > 128:
            raise ValueError('Maximum meeting_code length is 128 characters.')
        if passcode and len(passcode) > 128:
            raise ValueError('Maximum passcode length is 128 characters.')
        if password and len(password) > 128:
            raise ValueError('Maximum password length is 128 characters.')

        self.entry_point_type = entry_point_type
        self.uri = uri
        self.label = label
        self.pin = pin
        self.access_code = access_code
        self.meeting_code = meeting_code
        self.passcode = passcode
        self.password = password


class ConferenceSolution(_BaseConferenceSolution):
    """Information about the conference solution, such as Hangouts or Google Meet."""

    def __init__(
            self,
            entry_points,
            solution_type=None,
            name=None,
            icon_uri=None,
            conference_id=None,
            signature=None,
            notes=None
    ):
        """
        :param entry_points:
                :py:class:`~gcsa.conference.EntryPoint` or list of :py:class:`~gcsa.conference.EntryPoint`.
                Information about individual conference entry points, such as URLs or phone numbers.
                All of them must belong to the same conference.
        :param solution_type:
                Solution type. See :py:class:`~gcsa.conference.SolutionType`

                The possible values are:

                * HANGOUT - for Hangouts for consumers (hangouts.google.com)
                * NAMED_HANGOUT - for classic Hangouts for Google Workspace users (hangouts.google.com)
                * HANGOUTS_MEET - for Google Meet (meet.google.com)
                * ADD_ON - for 3P conference providers

        :param name:
                The user-visible name of this solution. Not localized.
        :param icon_uri:
                The user-visible icon for this solution.
        :param conference_id:
                The ID of the conference. Optional.
                Can be used by developers to keep track of conferences, should not be displayed to users.

                Values for solution types (see :py:class:`~gcsa.conference.SolutionType`):

                * HANGOUT: unset
                * NAMED_HANGOUT: the name of the Hangout
                * HANGOUTS_MEET: the 10-letter meeting code, for example "aaa-bbbb-ccc"
                * ADD_ON: defined by 3P conference provider

        :param signature:
                The signature of the conference data.
                Generated on server side. Must be preserved while copying the conference data between events,
                otherwise the conference data will not be copied.
                None for a conference with a failed create request.
                Optional for a conference with a pending create request.
        :param notes:
                String of additional notes (such as instructions from the domain administrator, legal notices)
                to display to the user. Can contain HTML. The maximum length is 2048 characters
        """
        super().__init__(conference_id=conference_id, signature=signature, notes=notes)
        self.entry_points = [entry_points] if isinstance(entry_points, EntryPoint) else entry_points
        self.solution_type = solution_type
        self.name = name
        self.icon_uri = icon_uri


class ConferenceSolutionRequest(_BaseConferenceSolution):
    """
    A request to generate a new conference and attach it to the event.
    The data is generated asynchronously. To see whether the data is present check the status field.
    """

    def __init__(
            self,
            solution_type=None,
            request_id=None,
            _status=None,
            conference_id=None,
            signature=None,
            notes=None
    ):
        """
        :param solution_type:
                Solution type. See :py:class:`~gcsa.conference.SolutionType`

                The possible values are:

                * HANGOUT - for Hangouts for consumers (hangouts.google.com)
                * NAMED_HANGOUT - for classic Hangouts for Google Workspace users (hangouts.google.com)
                * HANGOUTS_MEET - for Google Meet (meet.google.com)
                * ADD_ON - for 3P conference providers

        :param request_id:
                The client-generated unique ID for this request.
                By default it is generated as UUID.
                If you specify request_id manually, they should be unique for every new CreateRequest,
                otherwise request will be ignored.
        :param _status:
                The current status of the conference create request. Read-only.

                The possible values are:

                * "pending": the conference create request is still being processed.
                * "success": the conference create request succeeded, the entry points are populated.
                * "failure": the conference create request failed, there are no entry points.

        :param conference_id:
                The ID of the conference. Optional.
                Can be used by developers to keep track of conferences, should not be displayed to users.

                Values for solution types (see :py:class:`~gcsa.conference.SolutionType`):

                * HANGOUT: unset
                * NAMED_HANGOUT: the name of the Hangout
                * HANGOUTS_MEET: the 10-letter meeting code, for example "aaa-bbbb-ccc"
                * ADD_ON: defined by 3P conference provider

        :param signature:
                The signature of the conference data.
                Generated on server side. Must be preserved while copying the conference data between events,
                otherwise the conference data will not be copied.
                None for a conference with a failed create request.
                Optional for a conference with a pending create request.
        :param notes:
                String of additional notes (such as instructions from the domain administrator, legal notices)
                to display to the user. Can contain HTML. The maximum length is 2048 characters
        """
        super().__init__(conference_id=conference_id, signature=signature, notes=notes)
        self.request_id = request_id or uuid4().hex
        self.solution_type = solution_type
        self.status = _status
