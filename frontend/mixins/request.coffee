reqwest = require 'reqwest'

module.exports = (params) ->
  csrf_token = document.querySelector('meta[itemprop="csrf-token"]')?['content']
  defaults =
    type: 'json'
    method: 'get'
    contentType: 'application/json'
    withCredentials: true
    headers:
      'X-CSRFToken': csrf_token

  payload = Object.assign({}, defaults, params)
  if payload.method isnt 'get' and payload.data?
    payload.data = JSON.stringify(payload.data)

  reqwest(payload)
