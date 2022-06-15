import types
import inspect
import pytest


failed_conditions = []
xfailed_conditions = []


def soft_assert(assert_condition, message=None, xfail=False):
    global failed_conditions
    global xfailed_conditions
    if isinstance(assert_condition, types.FunctionType):
        try:
            assert_condition()
        except AssertionError as error:
            if xfail:
                add_xfailed(message if message else error)
            else:
                add_exception(message if message else error)
    else:
        try:
            assert assert_condition
        except AssertionError:
            if xfail:
                add_xfailed(message if message else error)
            else:
                add_exception(message if message else 'Failed by assertion!')


def verify_expectations():
    global failed_conditions
    global xfailed_conditions
    if failed_conditions or xfailed_conditions:
        report_exceptions()


def add_exception(message=None):
    global failed_conditions
    (file_path, line, function_name) = inspect.stack()[2][1:4]
    failed_conditions.append('Exception: {}\nFail in "{}:{}" {}()\n'.format(message, file_path, line, function_name))


def add_xfailed(message=None):
    global xfailed_conditions
    (file_path, line, function_name) = inspect.stack()[2][1:4]
    xfailed_conditions.append('Exception: {}\nFail in "{}:{}" {}()\n'.format(message, file_path, line, function_name))


def report_exceptions():
    global failed_conditions
    global xfailed_conditions
    report = []
    xreport = []
    if failed_conditions:
        report = ['Failed conditions count: [ {} ]\n'.format(len(failed_conditions))]
        for index, failure in enumerate(failed_conditions, start=1):
            if len(failed_conditions) > 1:
                report.append('{}. {}'.format(index, failure))
            else:
                report.append(failure)
        failed_conditions = []
    if xfailed_conditions:
        xreport = ['XFailed conditions count: [ {} ]\n'.format(len(xfailed_conditions))]
        for index, failure in enumerate(xfailed_conditions, start=1):
            if len(xfailed_conditions) > 1:
                xreport.append('{}. {}'.format(index, failure))
            else:
                xreport.append(failure)
        xfailed_conditions = []
    if report:
        report += xreport
        raise AssertionError('\n'.join(report))
    elif xreport:
        pytest.xfail('\n'.join(xreport))
