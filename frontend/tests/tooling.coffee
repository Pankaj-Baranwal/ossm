'use strict'
require './helper'
{expect} = require 'chai'

describe 'Components', ->
  it 'should exist', ->
    expect(require 'ossm').to.be.a 'function'

