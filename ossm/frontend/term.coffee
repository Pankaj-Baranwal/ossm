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
    cargs = cargs.trim()
    cargs = cargs.split " "
    switch cargs[0]
      when 'help', '?' then return @help cargs.splice 1, cargs.length - 1
      when 'event' then return @event cargs.splice 1, cargs.length - 1
      when 'takeme' then return @navigate cargs.splice 1, cargs.length - 1
      when 'exit' then return @exit cargs.splice 1, cargs.length - 1
      else return 'Nope. Wrong Command.'

  help: (args) ->
    if args.length > 0 then return "unknown option(s): #{ args }"
    return "available commands:\n
            help (or ?) - show help and exit\n
            event [event_name] - do something with events\n
            takeme [location] - navigate around the website\n
            exit - minimize this terminal\n
            tip - use ? at the end of any command to see its help"

  navigate: (args) ->
    window.location = url
    return 'Namaste!'

  event: (args) ->
    switch args[1]
      when 'ossome' then
    return 'Ooh! You seem excited for the events!'


module.exports = Terminal
