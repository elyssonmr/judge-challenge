# Judge Challenge

Judge Challenge is an open source project to easily promote coding challanges.

## What is Judge Chanllenge?

A platform to help promoting coding challenges. It could be used in internal or external challanges of your organization.

The platform uses Docker to isolate the test execution, providing more security for executing third party code and to enable as many tecnologies suported by docker. It also provide tools to track the history of the challengers acomplhishments. 

## Contributing

To contribute with the project, you could just put your name in one of the opened issues, do some work ofr the issue and open a new Pull Request.

In the case of doubt we could discuss what is to be done in the comments section of the issue with other people too.

Every issue will be tagged with a dificult label according of the reporter intuition. The difficult is not "written in stone", we could also discuss and change the label as needed.


## MVP (First Release)

In this release we are going to create a simple version of the project.

The fisrt runner is a Python + Pytest runner that could validate almost all Unit Test cases. Of course it would not cover some edge cases or case with other libraries, but it will help to create and validate the infrastructure needed to run the challenge tests.

The interface to comunicate with the platform is a API to create the challenges with its tests and to enable code submission from the users. At first it would just inform if the tests passed, if there is some kind of error (in this case we are going to return the entire terminal output from the container) or if a timeout occured.