from __future__ import print_function

from testrail import TestRail

tr = TestRail(15)
print("\nactive_plans", list(tr.active_plans()))
print("\nactive_suites", list(tr.active_suites()))
print("\nactive_users", list(tr.active_users()))
print("\ninactive_users", list(tr.inactive_users()))
print("\ncompleted_plans", list(tr.completed_plans()))
print("\ncompleted_suites", list(tr.completed_suites()))
print("\nmilestones", list(tr.milestones()))
print("\nplans", list(tr.plans()))
print("\nprojects", list(tr.projects()))
print("\nruns", list(tr.runs())[:10])
print("\nstatuses", list(tr.statuses())[:10])
print("\nsuites", list(tr.suites())[:10])
print("\nusers", list(tr.users())[:10])
print("\nconfigs", list(tr.configs())[:10])
print("\ncases", list(tr.cases(list(tr.suites())[0]))[:10])
print("\ntests", list(tr.tests(list(tr.runs())[0]))[:10])
print("\nresults",list(tr.results(list(tr.tests(list(tr.runs())[0]))[0]))[:10])
