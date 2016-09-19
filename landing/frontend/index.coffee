request = require('mixins/request')


class Subscribe
  ENDPOINT: '/api/v1/people/subscription/'
  constructor: ->
    # Event handle.
    @btn = document.querySelector('#subscription button')
    @input = document.querySelector('#subscription input')
    @form = document.getElementById('subscription')

    @form.addEventListener 'submit', (e) =>
      e.preventDefault()
      @handleSubmit()

  handleSubmit: ->
    @btn.disabled = yes
    @btn.style.backgroundColor = 'gray'
    @input.disabled = yes

    request url: @ENDPOINT, method: 'POST', data: email: @input.value
      .then (response) =>
        @btn.innerHTML = 'Subscribed'
        @btn.style.backgroundColor = 'green'
      .fail (err) =>
        if err.status is 400 then @btn.innerHTML = 'Already Subscribed!'
        else @btn.innerHTML = 'Error'
      .always () =>
        setTimeout =>
          @btn.innerHTML = 'Subscribe'
          @btn.style.backgroundColor = '#007ea7'
          @btn.disabled = no
          @input.disabled = no
          @input.value = ''
        , 1500


module.exports = ->
  new Subscribe
