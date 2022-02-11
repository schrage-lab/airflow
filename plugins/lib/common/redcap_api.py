import requests
import os
from dotenv import load_dotenv


"""module to make API calls to REDCap"""


class PostAPI:
    """decorator class for wrapping and making redcap_api calls to REDCap"""

    def __init__(self, func):
        self.func = func
        self.token = None
        self.url = None
        self.get_config_info()

    def __call__(self, *args, **kwargs):
        # get specific post parameters being sought
        post = self.func(*args, **kwargs)

        # add token to post parameters
        post['token'] = self.token

        # make request
        request = requests.post(self.url, data=post)

        # check response code, throw error if necessary
        self.parse_api_response(request)

        # return json data from API call
        return request.json()

    def get_config_info(self) -> None:
        fpath = os.path.abspath(os.path.relpath('plugins', os.path.dirname(__file__)))
        load_dotenv(dotenv_path=fpath)
        self.token = os.getenv('redcap_token')
        self.url = os.getenv('redcap_url')

    def log_api_response(self):
        # todo: create log?
        pass

    @staticmethod
    def parse_api_response(request):
        if request.status_code == 200:
            pass
        elif request.status_code == 400:
            # todo: build logger
            ValueError(f"{request.status_code}: {request.reason}")
        elif request.status_code == 401:
            ValueError(f"Error {request.status_code}: API token is missing or incorrect.")
        elif request.status_code == 403:
            PermissionError(f"Error {request.status_code}: You do not have permissions to use the API.")
        elif request.status_code == 404:
            ValueError(f"Error {request.status_code}: The URI you requested is invalid or the resource does not exist.")
        elif request.status_code == 406:
            ValueError(f"Error {request.status_code}: The data being imported was formatted incorrectly.")
        elif request.status_code == 500:
            ConnectionError(f"Error {request.status_code}: The server encountered an error processing your request.")
        elif request.status_code == 501:
            ValueError(f"Error {request.status_code}: The requested method is not implemented.")


@PostAPI
def export_arms(arms: list = None, data_format: str = 'json', error_format: str = 'json', *args, **kwargs) -> dict:
    # todo: add documentation

    post = {
        'content': 'arm',
        'format': data_format,
        'returnFormat': error_format
    }

    if arms is not None:
        post = _helper_to_add_key_values_to_post_dict('arms', list(arms), post)

    return post


@PostAPI
def export_events(arms: list = None, post_format: str = 'json', data_format: str = 'json', *args, **kwargs):
    # todo: add documentation

    post = {
        'content': 'event',
        'format': post_format,
        'returnFormat': data_format
    }

    if arms is not None:
        post = _helper_to_add_key_values_to_post_dict('arms', list(arms), post)

    return post


@PostAPI
def export_field_names(fields: list = None, data_format: str = 'json', error_format: str = 'json', *args, **kwargs):
    """
    This method returns a list of the export/import-specific version of field names for all fields (or for one field,
    if desired) in a project. This is mostly used for checkbox fields because during data exports and data imports,
    checkbox fields have a different variable name used than the exact one defined for them in the Online Designer and
    Data Dictionary, in which *each checkbox option* gets represented as its own export field name in the following
    format: field_name + triple underscore + converted coded value for the choice. For non-checkbox fields, the export
    field name will be exactly the same as the original field name. Note: The following field types will be
    automatically removed from the list returned by this method since they cannot be utilized during the data import
    process: 'calc', 'file', and 'descriptive'.

    The list that is returned will contain the three following attributes for each field/choice: 'original_field_name',
    'choice_value', and 'export_field_name'. The choice_value attribute represents the raw coded value for a checkbox
    choice. For non-checkbox fields, the choice_value attribute will always be blank/empty. The export_field_name
    attribute represents the export/import-specific version of that field name.
    """

    post = {
        'content': 'exportFieldNames',
        'format': data_format,
        'returnFormat': error_format
    }

    if fields is not None:
        post = _helper_to_add_key_values_to_post_dict('fields', list(fields), post)

    return post


@PostAPI
def export_file(record_id: str, field_name: str, event: str, repeat_instance: str, data_format: str = 'json', *args,
                **kwargs):
    """
    This method allows you to download a document that has been attached to an individual record for a File Upload
    field. Please note that this method may also be used for Signature fields (i.e. File Upload fields with 'signature'
    validation type).

    Note about export rights: Please be aware that Data Export user rights will be applied to this API request. For
    example, if you have 'No Access' data export rights in the project, then the API file export will fail and return an
    error. And if you have 'De-Identified' or 'Remove all tagged Identifier fields' data export rights, then the API
    file export will fail and return an error *only if* the File Upload field has been tagged as an Identifier field. To
    make sure that your API request does not return an error, you should have 'Full Data Set' export rights in the
    project.
    """

    # todo: finish method and make args consistent
    post = {
        'content': 'file',
        'action': 'export',
        'record': record_id,
        'field': field_name,
        'event': event,
        'repeat_instance': repeat_instance,
        'returnFormat': data_format
    }

    return post


@PostAPI
def export_form_event_mapping(arms: list = None, data_format: str = 'json', error_format: str = 'json', *args,
                              **kwargs):
    # todo: add documentation

    post = {
        'content': 'formEventMapping',
        'format': data_format,
        'returnFormat': error_format
    }
    if arms is not None:
        post = _helper_to_add_key_values_to_post_dict('arms', list(arms), post)
    return post


@PostAPI
def export_metadata(fields: list = None, forms: list = None, data_format: str = 'json', error_format: str = 'json',
                    *args, **kwargs):
    # todo: add documentation

    post = {
        'content': 'metadata',
        'format': data_format,
        'returnFormat': error_format
    }

    # add specific fields, if passed
    if fields is not None:
        post = _helper_to_add_key_values_to_post_dict('fields', fields, post)

    # add specific forms, if passed
    if forms is not None:
        post = _helper_to_add_key_values_to_post_dict('forms', forms, post)

    return post


@PostAPI
def export_logging(log_type: str = 'all', user: str = None, record_id: str = None, dag: str = None,
                   begin_time: str = None, end_time: str = None, data_format: str = 'json',
                   error_format: str = 'json', *args, **kwargs):
    """
    This method allows you to export the logging (audit trail) of all changes made to this project, including data
    exports, data changes, project metadata changes, modification of user rights, etc.

    :param log_type: You may choose event type to fetch result for specific event type. Options: 'all', 'data_export',
        'manage_design', 'user_role_cud', 'record_cud', 'record_create', 'record_updated', 'record_deleted',
        'record_locking_esignatures', 'page_views'. Default: 'all'. *Note: when returning 'all', it excludes page views.

    :param user: To return only the events belong to specific user (referring to existing username), provide a user. If
        not specified, it will assume all users.

    :param record_id: To return only the events belong to specific record (referring to existing record name), provide
        a record. If not specified, it will assume all records. This parameter is available only when event is related
        to record.

    :param dag: To return only the events belong to specific DAG (referring to group_id), provide a dag. If not
        specified, it will assume all dags.

    :param begin_time: To return only the events that have been logged *after* a given date/time, provide a timestamp in
        the format YYYY-MM-DD HH:MM (e.g., '2017-01-01 17:00' for January 1, 2017 at 5:00 PM server time). If not
        specified, it will assume no begin time. If only a date is passed, the time will default to
        12:00 AM server time.

    :param end_time: To return only records that have been logged *before* a given date/time, provide a date or a
        timestamp in the format YYYY-MM-DD HH:MM (e.g., '2017-01-01 17:00' for January 1, 2017 at 5:00 PM server time).
        If not specified, it will use the current server time. If only a date is passed, the time will default to
        11:59 PM server time.

    :param data_format: Specifies the format that data are returned. Options: 'csv', 'json', 'xml'. Default: 'json'.

    :param error_format: Specifies the format of error messages. If you do not pass in this flag, it will select the
        default format for you passed based on the 'data_format' flag you passed in. Options: 'csv', 'json', 'xml'.
        Default: 'json'.
    """

    log_types = ['all', 'data_export', 'manage_design', 'user_role_cud', 'record_cud', 'record_create',
                 'record_updated', 'record_deleted', 'record_locking_esignatures', 'page_views']

    if log_type not in log_types:
        ValueError(f"Export Logging: Invalid log type f{log_type}")

    # todo: check for user in list of users
    # todo: check that record_id exists in project
    # todo: check dag

    # todo: finish function
    post = {
        'content': 'log',
        'format': data_format,
        'logType': log_type,
        'returnFormat': error_format
    }
    return post


@PostAPI
def export_records(records: list = None, fields: list = None, forms: list = None, events: list = None,
                   raw_or_label: str = 'raw', raw_or_label_headers: str = 'raw', export_checkbox_label: bool = False,
                   export_survey_fields: bool = False, export_dags: bool = False, filter_logic: str = None,
                   date_range_begin: str = None, date_range_end: str = None, csv_delimiter: str = 'comma',
                   decimal_char: str = None, return_type: str = 'flat', data_format: str = 'json',
                   error_format: str = 'json', *args, **kwargs) -> dict:
    """This method allows you to export a set of records for a project.

    :param records: An array of record names specifying specific records you wish to pull. If 'None', all records will
        be pulled. Default: 'None'.

    :type records: list

    :param fields: An array of field names specifying specific fields you wish to pull. If 'None', all fields will be
        pulled. Default: 'None'.

    :type fields: list

    :param forms: An array of form names you wish to pull records for. If 'None', then all forms will be pulled.
        Default: 'None'

    :type forms: list

    :param events: An array of unique event names that you wish to pull records for. If 'None', all events will be
    pulled. Default: 'None'. *Note: only for longitudinal projects.

    :type events: list

    :param raw_or_label: Export the raw coded values or labels for the options of multiple choice fields. Options:
        'raw', 'label'. Default: 'raw'.

    :type raw_or_label: str

    :param raw_or_label_headers: For the CSV headers, export the variable/field names (raw) or the field labels (label).
        Options: 'raw', 'label'. Default: 'raw'. *Note: for 'csv' format 'flat' type only.

    :type raw_or_label_headers: str

    :param export_checkbox_label: Specifies the format of checkbox field values specifically when exporting the data as
        labels (i.e., when raw_or_label=label) in flat format (i.e., when return_type=flat). When exporting labels, by
        default (if export_checkbox_label=false), all checkboxes will either have a value 'Checked' if they are checked
        or 'Unchecked' if not checked. But if export_checkbox_label is set to true, it will instead export the
        checkbox value as the checkbox option's label (e.g., 'Choice 1') if checked or it will be blank/empty (no value)
        if not checked. If raw_or_label=false or if return_type=eav, then the export_checkbox_label flag is ignored.
        (The export_checkbox_label parameter is ignored for return_type=eav because 'eav' type always exports checkboxes
        differently anyway, in which checkboxes are exported with their true variable name (whereas the 'flat' type
        exports them as variable___code format), and another difference is that 'eav' type *always* exports checkbox
        values as the choice label for labels export, or as 0 or 1 (if unchecked or checked, respectively) for raw
        export.). Default: False.

    :type export_checkbox_label: bool

    :param export_survey_fields: Specifies whether or not to export the survey identifier field
        (e.g., 'redcap_survey_identifier') or survey timestamp fields (e.g., instrument+'_timestamp') when surveys are
        utilized in the project. If set to 'true', it will return the redcap_survey_identifier field and also the survey
        timestamp field for a particular survey when at least one field from that survey is being exported. *NOTE: If
        the survey identifier field or survey timestamp fields are imported via API data import, they will simply be
        ignored since they are not real fields in the project but rather are pseudo-fields. Default: False.

    :type export_survey_fields: bool

    :param export_dags: Specifies whether or not to export the 'redcap_data_access_group' field when data access groups
        are utilized in the project. *NOTE: This flag is only viable if the user whose token is being used to make the
        API request is *not* in a data access group. If the user is in a group, then this flag will revert to its
        default value. Default: False.

    :type export_dags: bool

    :param filter_logic: String of logic text (e.g., [age] > 30) for filtering the data to be returned by this API
        method, in which the API will only return the records (or record-events, if a longitudinal project) where the
        logic evaluates as TRUE. *NOTE: if the filter logic contains any incorrect syntax, the API will respond with an
        error message.

    :type filter_logic: str

    :param date_range_begin: A timestamp to return only records that have been created or modified after a given
        date/time. Format is YYYY-MM-DD HH:MM:SS (e.g., '2017-01-01 00:00:00' for January 1, 2017 at
        midnight server time). If 'None', it will assume no begin time. Default: 'None'.

    :type date_range_begin: str

    :param date_range_end: A timestamp to return only records that have been created or modified before a given
        date/time. Format is YYYY-MM-DD HH:MM:SS (e.g., '2017-01-01 00:00:00' for January 1, 2017 at
        midnight server time). If 'None', it will assume no end time. Default: 'None'.

    :type date_range_end: str

    :param csv_delimiter: Set the delimiter used to separate values in the CSV data file. Options: 'comma', 'tab',
        'semicolon', 'pipe', or 'caret'. Default: 'comma'. *NOTE: for CSV format only.

    :type csv_delimiter: str

    :param decimal_char: If specified, force all numbers into same decimal format. You may choose to force all data
        values containing a decimal to have the same decimal character, which will be applied to all calc fields and
        number-validated text fields. Options: 'comma', 'dot'.  If 'None', numbers will be exported using the fields'
        native decimal format.

    :type decimal_char: str

    :param return_type: Specifies the method in which returned data is modeled. 'flat' option outputs one record per
        row. 'eav' option outputs one data point per row. *Note: For non-longitudinal studies, the fields will be
        record, field_name, value. For longitudinal studies, the fields will be record, field_name, redcap_event_name.
        Options: 'flat', 'eav'. Default: 'flat'.

    :type return_type: str

    :param data_format: Specifies the format that data are returned. Options: 'csv', 'json', 'xml'. Default: 'json'.

    :type data_format: str

    :param error_format: Specifies the format of error messages. If you do not pass in this flag, it will select the
        default format for you passed based on the 'data_format' flag you passed in. Options: 'csv', 'json', 'xml'.
        Default: 'json'.

    :type error_format: str
    """

    post = {
        'content': 'record',
        'rawOrLabel': raw_or_label,
        'rawOrLabelHeaders': raw_or_label_headers,
        'exportCheckboxLabel': str(export_checkbox_label),
        'exportSurveyFields': str(export_survey_fields),
        'exportDataAccessGroups': str(export_dags),
        'type': return_type,
        'returnFormat': error_format,
        'format': data_format
    }

    # add filter logic, if passed
    if filter_logic is not None:
        post['filterLogic'] = filter_logic

    # add date begin, if passed
    if date_range_begin is not None:
        post['dateRangeBegin'] = date_range_begin

    # add date end, if passed
    if date_range_end is not None:
        post['dateRangeEnd'] = date_range_end

    # translate the csv_delimiter arg to the appropriate string for the API call
    # note: don't need to translate 'tab'
    if csv_delimiter.lower() == 'comma':
        csv_delimiter = ','
    elif csv_delimiter.lower() == 'semicolon':
        csv_delimiter = ';'
    elif csv_delimiter.lower() == 'pipe':
        csv_delimiter = '|'
    elif csv_delimiter.lower() == 'caret':
        csv_delimiter = '^'
    post['csvDelimiter'] = csv_delimiter

    # translate the decimal_char arg to the appropriate string for the API call
    if decimal_char is not None:
        if decimal_char == 'comma':
            decimal_char = ','
        elif decimal_char == 'dot':
            decimal_char = '.'
        post['decimalCharacter'] = decimal_char

    # add specific records, if passed
    if records is not None:
        post = _helper_to_add_key_values_to_post_dict('records', records, post)

    # add specific fields, if passed
    if fields is not None:
        post = _helper_to_add_key_values_to_post_dict('fields', fields, post)

    # add specific forms, if passed
    if forms is not None:
        post = _helper_to_add_key_values_to_post_dict('forms', forms, post)

    # add specific events, if passed
    if events is not None:
        post = _helper_to_add_key_values_to_post_dict('events', events, post)

    return post


@PostAPI
def import_records(data: dict, records: list = None, overwrite: bool = False, auto_number: bool = False,
                   data_type: str = 'flat', date_format: str = 'YMD', return_content: str = 'count',
                   csv_delimiter: str = 'comma', data_format: str = 'json', error_format: str = 'json', *args,
                   **kwargs):
    # todo: add documentation

    post = {
        'content': 'record',
        'data': data,
        'type': data_type,
        'forceAutoNumber': str(auto_number),
        'returnContent': return_content,
        'format': data_format,
        'returnFormat': error_format,
        'dateFormat': date_format
    }

    # translate overwrite argument to the appropriate string for the API call
    if overwrite is False:
        overwrite_str = 'normal'
    else:
        overwrite_str = 'overwrite'
    post['overwriteBehavior'] = overwrite_str

    # translate the csv_delimiter arg to the appropriate string for the API call
    # note: don't need to translate 'tab'
    if csv_delimiter.lower() == 'comma':
        csv_delimiter = ','
    elif csv_delimiter.lower() == 'semicolon':
        csv_delimiter = ';'
    elif csv_delimiter.lower() == 'pipe':
        csv_delimiter = '|'
    elif csv_delimiter.lower() == 'caret':
        csv_delimiter = '^'
    post['csvDelimiter'] = csv_delimiter

    # add specific records, if passed
    if records is not None:
        post = _helper_to_add_key_values_to_post_dict('records', records, post)

    return post


def _helper_to_add_key_values_to_post_dict(key_basename: str, values_list: list, post_dict: dict) -> dict:
    for idx, value in enumerate(values_list):
        post_dict[f'{key_basename}[{idx}]'] = value
    return post_dict


if __name__=='__main__':
    print(export_arms())
