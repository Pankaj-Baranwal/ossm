rivets = require 'rivets'


class Terminal
  constructor: (container) ->
    @term =
      visible: no
      busy: no
      buffer: []
      input: ''
      onToggle: => @term.visible = !@term.visible
      onFocus: => if @term.visible then @_input_el.focus()
      onKeyUp: (e) =>
        if e.keyCode is 13 then @trigger()
    @_buf_el = container.querySelector('ul')
    @_input_el = container.querySelector('input')
    @_view = rivets.bind container, @term

    @term.visible = /^\/$/.test window.location.pathname

  trigger: ->
    varg = @term.input
    @term.busy = yes
    @appendToBuffer '~ ' + varg
    switch
      when varg == '' or /[ ]+$/.test varg then @appendToBuffer()
      when /help/.test varg then @appendToBuffer 'We need help too.'
      when /^:wq/.test varg then window.location = 'google.com'
      else @appendToBuffer 'Nope. Wrong Command.'
    @term.busy = no
    @term.input = ''

  appendToBuffer: (value) ->
    @term.buffer.push value
    @_buf_el.lastElementChild.scrollIntoView()


module.exports = Terminal
