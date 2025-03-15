$(document).ready(function () {
    $('.log-challenge-btn').off('click').on('click', function () {
        var challengeId = $(this).data('challenge-id');
        var logUrl = $(this).data('log-url').replace('0', challengeId);
        if (confirm('Are you sure you want to log this challenge? No cheating, dishonesty is not very Eco friendly.')) {
            window.location.href = logUrl;
        }
    });

    $('.like-challenge-btn').off('click').on('click', function () {
        var challengeId = $(this).data('challenge-id');
        var likeUrl = $(this).data('like-url'); // Get the URL from the data attribute
        var button = $(this);

        $.post(likeUrl, {
            challenge_id: challengeId,
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        }, function (data) {
            if (data.success) {
                $('#likes-' + challengeId).text(data.likes);
                button.prop('disabled', true);
            } else {
                alert(data.message);
            }
        });
    });

    $('#update-picture-btn').off('click').on('click', function () {
        $('#update-picture-modal').modal('show');
    });

    $('#update-email-btn').off('click').on('click', function () {
        $('#update-email-modal').modal('show');
    });

    $('#update-picture-form').off('submit').on('submit', function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                alert('Profile picture updated successfully');
                location.reload();
            },
            error: function (response) {
                alert('An error occurred while updating the profile picture');
            }
        });
    });

    $('#update-email-form').off('submit').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                alert('Email updated successfully');
                location.reload();
            },
            error: function (response) {
                alert('An error occurred while updating the email');
            }
        });
    });

    $('select[name="timeframe"]').change(function () {
        $(this).closest('form').submit();
    });

    $('#search-input').on('input', function () {
        const query = $(this).val();

        $.ajax({
            url: '{% url "Eco:search_educational_links" %}',
            data: {
                'q': query
            },
            dataType: 'json',
            success: function (data) {

                data.forEach(function (link) {
                    const newItem = `<li><a href="${link.fields.url}" target="_blank"><strong>${link.fields.title}</strong></a> – ${link.fields.description}</li>`;
                });
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error: " + status + error);
            }
        });
    });
});

$(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});