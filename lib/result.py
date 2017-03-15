import sys
class TermColors:
    ''' Collection of colors for printing out to terminal '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

ignoredFields = {'Age', 'Set-Cookie', 'Server', 'Date'}
class Result(object):
    ''' Result encapsulates the result of a single session replay '''

    def __init__(self, test_name, expected_response, received_response, recv_resp_body=None):
        ''' expected_response and received_response can be any datatype the caller wants as long as they are the same datatype '''
        self._test_name = test_name
        self._expected_response = expected_response
        self._received_response = received_response
        self._received_response_body = recv_resp_body

    def getTestName(self):
        return self._test_name

    def getResultBool(self):
        return self._expected_response == self._received_response

    def getRespBody(self):
        if self._received_response_body:
            return self._received_response_body
        else:
            return ""
    def Compare(self, received_dict, expected_dict):
        global ignoredFields
        for key in received_dict:
            if key in expected_dict and key not in ignoredFields:
                if received_dict[key]!=expected_dict[key]:
                    print("{0}Difference in the field \"{1}\": \n received:\n{2}\n expected:\n{3}{4}".format(TermColors.FAIL,key,received_dict[key],expected_dict[key],TermColors.ENDC))
                    return False
        return True
        
    def getResultString(self, received_dict, expected_dict, colorize=False ):
        global ignoredFields
        ''' Return a nicely formatted result string with color if requested '''
        if self.getResultBool() and self.Compare(received_dict,expected_dict):
            if colorize:
                outstr = "{0}PASS{1}".format(
                    TermColors.OKGREEN, TermColors.ENDC)

            else:
                outstr = "PASS"

        else:
            if colorize:
                outstr = "{0}FAIL{1}: expected {2}, received {3}, session file: {4}".format(
                    TermColors.FAIL, TermColors.ENDC, self._expected_response, self._received_response, self._test_name)

            else:
                outstr = "FAIL: expected {0}, received {1}".format(
                    self._expected_response, self._received_response)
                sys.exit(0)

        return outstr
