# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s infoporto.pim -t test_message.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src infoporto.pim.testing.INFOPORTO_PIM_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_message.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Message
  Given a logged-in site administrator
    and an add message form
   When I type 'My Message' into the title field
    and I submit the form
   Then a message with the title 'My Message' has been created

Scenario: As a site administrator I can view a Message
  Given a logged-in site administrator
    and a message 'My Message'
   When I go to the message view
   Then I can see the message title 'My Message'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add message form
  Go To  ${PLONE_URL}/++add++Message

a message 'My Message'
  Create content  type=Message  id=my-message  title=My Message


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the message view
  Go To  ${PLONE_URL}/my-message
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a message with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the message title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
