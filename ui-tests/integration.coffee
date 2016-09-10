chai = require 'chai'
chai_webdriver = require 'chai-webdriver'
webdriver = require 'selenium-webdriver'

driver = new webdriver.Builder()
  .withCapabilities(webdriver.Capabilities.phantomjs())
  .build()
chai.use chai_webdriver(driver)
{expect} = chai

after ->
  driver.quit()


describe 'UI Integration', ->

  # before ->
  #   driver.get('https://noop.pw')

  # it 'should use phantomjs to render', ->
  #   expect('h1').dom.to.be.ok
