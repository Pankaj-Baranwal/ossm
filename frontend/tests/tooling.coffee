'use strict'
require './helper'
{expect} = require 'chai'

describe 'Components', ->
  it 'should exist', ->
    expect(require_app 'ossm').to.be.a 'function'

