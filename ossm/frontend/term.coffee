rivets = require 'rivets'


class Terminal
  constructor: (container) ->
    @term =
      visible: yes
      busy: no
      buffer: []
      input: ''
      onKeyUp: (e) =>
        if e.keyCode is 13 then @trigger()
    @_buf_el = container.querySelector('ul')
    @_view = rivets.bind container, @term

  trigger: ->
    varg = @term.input
    @term.busy = yes
    switch
      when /help/.test varg then @appendToBuffer 'We need help too.'
      when /^:wq/.test varg then window.location = 'google.com'
      else @appendToBuffer 'Nope. Wrong Command.'
    @term.busy = no
    @term.input = ''

  appendToBuffer: (value) ->
    @term.buffer.push value
    @_buf_el.lastElementChild.scrollIntoView()


module.exports = Terminal
