
### Requirements:
 * Python 3.10.7
 * Playwright 1.28.0 
 * Pytest 7.2.0


### Script options:
- *base_url* (pytest.ini) = base url that is used to get Homepage url -> may be overwritten by *--home_url_preset*
- *--home_url_preset* = when specified: testing starts from provided url (get homepage url method is skipped)
- *--country* = Corresponds to _country_ on start-up page
- *--city* = Corresponds to _city_ on start-up page

```
Three run options explained:

I.  Run without any parameters - randomly choosen country & city
> pytest

II. Run with country & city specified
> pytest --country='Saudi Arabia' --city=Jeddah

III.Run with '--home_url_preset' option (country & city are not specified)
> pytest --home_url_preset=https://floward.com/en-sa/mecca
```
---
#### NOTE:
Accordingly, to test flow:
> Steps to be Automated:
</br> i. Navigate to Home Page
</br> ii. Click on any Category
</br> iii. Go to Product Listing Page
</br> iv. Select any Product
</br> v. To click an “Add to cart” button
</br> vi. Finally, to verify the success message.

Last step assumed to be on 'checkout/cart' screen.

In the need to continue test flow - authorization required.

'Card Message' (data-testid="TestId__CardMessage") visible - accepted as successful test result message.

---
```
The below questions have to be explained.


I. Criteria's for finalizing the technologies

Answer: 
was decided to write a test on Python + Playwright

for the provided purpose it suits well with proper speed abilities, flexibility, and browser setup.
feedback: It was interesting to make this test work on Playwright. 
It has a variety of different communications in the browser - with elements, dom, requests, etc.


II. Explain about the architecture of the framework

Answer: 
For further development, it makes sense to consider migrating the project to a Page Object pattern.
For now, the project has a small size and some configuration presets.
All automation steps are mainly explained in the comments.
It would be good to add logging, some more screenshots, or video capture.

The main test file is 'demo_test.py'.
- 'context' fixture run & close browser & context (once per session)
- 'homepage_url' get a proper homepage URL using provided options or random choice
- 'test_run' run the main test method
- Note: The product basket selection step is also automated
'conftest.py' - describes run options
'pytest.ini' - declare base_url and additional configuration
'requirements.txt' - represents the main build requirements

III. Explain about the CI/CD integration aspect

ci/cd requires a proper configuration approach.
It takes some time to prepare jobs, pipelines, and builds - but it gives good results.
On big projects, ci/cd requires appropriate unit and sanity tests that are small and effective enough. 
A good approach is to cover and integrate automation tests right in parallel with the development process. 
Well-suited development process allows the QA engineer to write tests in advance of dev realization - using agreed data-testid locators and user flows.
For the best results in terms of documentation and life product cycle, there are some effective approaches such as BDD, TDD, etc.

IV. Explain about the test result reporting and analysing aspect.

The best way of resulting reports is to install and configure any reporter plugin - such as Allure.
Specified steps and flexible configuration allows us to have proper reports that match our needs.
Also, it's useful (especially for manual testers) to have some integration with the test management system. (TestRail, TestStuff, etc.) 
Automation test results can be automatically imported into TMS with cases & steps and results specified. It helps to exclude already passed tests and focus on the one left. 
In addition, TMS can be used as a task manager for automation engineers.
```

Best regards, JSP.