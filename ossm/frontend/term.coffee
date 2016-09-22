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
    handler = new CommandHandler()
    @appendToBuffer handler.execute(varg)
    @term.busy = no
    @term.input = ''

  appendToBuffer: (value) ->
    @term.buffer.push value
    @_buf_el.lastElementChild.scrollIntoView()


class CommandHandler
  constructor: () ->
    return

  execute: (cargs) ->
    switch
      when cargs == '' or /[ ]+$/.test cargs then return ''
      when /help/.test cargs then return @help ''
      when /^:wq/.test cargs then return @navigate '//hashinclude.ducic.ac.in'
      else return 'Nope. Wrong Command.'

  help: (topic) ->
    return 'We need help too.'

  navigate: (url) ->
    window.location = url
    return 'Namaste!'


module.exports = Terminal
