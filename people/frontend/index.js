var $ = require('cash-dom');
var request = require('mixins/request');
var rivets = require('rivets');
console.log('people scripts init');

function resetButtons() {
    $('form').find('input').attr('disabled', 'disabled');
    $('#user-name-edit-button').css('visibility', 'visible');
    $('#user-name-update-button').css('visibility', 'collapse');
    $('#user-name-cancel-button').css('visibility', 'collapse');
}

function updateName() {
    $('#user-name-edit-button').attr('disabled', 'disabled');
    $('#user-name-update-button').attr('disabled', 'disabled');
    $('#user-name-cancel-button').attr('disabled', 'disabled');
    var fName = $('#user-first-name-input').val();
    var lName = $('#user-last-name-input').val();
    var data = new FormData();
    data.append('first_name', fName);
    data.append('last_name', lName);

    // west({
    //     url: '/rest-auth/user/',
    //     method: 'patch',
    //     data: data,
    //     success: function(resp) {
    //         console.log(resp);
    //     },
    //     error: function (err) {
    //         console.log(err);
    //     }
    // });
    $('#user-name-edit-button').removeAttr('disabled', 'disabled');
    $('#user-name-update-button').removeAttr('disabled', 'disabled');
    $('#user-name-cancel-button').removeAttr('disabled', 'disabled');
}

// $('#user-name-edit-button').on('click', function (e) {
//     $('form').find('input').removeAttr('disabled');
//     $('#user-name-edit-button').css('visibility', 'collapse');
//     $('#user-name-update-button').css('visibility', 'visible');
//     // $('#user-name-update-button').on('click', updateName);
//     $('#user-name-cancel-button').css('visibility', 'visible');
//     $('#user-name-cancel-button').on('click', resetButtons);
// });

module.exports = function () {
    $('button.register').each(function (button) {
        $(button).on('click', function () {
            var eventCode = $(this).data('event');
            request({
                url: '../events/register/',
                method: 'post',
                data: {
                    event: eventCode
                },
                success: function (resp) {
                    if (this.status in [200, 201, 202]) {
                        $(button).text('Registered');
                    }
                }
            });
        });
    });
};
