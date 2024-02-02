function updateTemplateAndSubject() {
    var templateId = document.getElementById("email-template").value;
    var subject = templateId === "1" ? "Subject 1" : "Subject 2";
    document.getElementById("email-subject").value = subject;

    fetch(`/get_template_content/${templateId}`)
        .then(response => response.json())
        .then(data => {
            if (data.content) {
                document.getElementById("template-preview").innerHTML = data.content;
                generateInputFields(data.content);
            } else {
                alert('Template not found');
            }
        })
        .catch(error => {
            alert('Error fetching template: ' + error);
        });
}

function generateInputFields(templateContent) {
    // Example regex to find placeholders like {{name}}
    const placeholderRegex = /\{\{(\w+)\}\}/g;
    let match;
    let inputFieldsContainer = document.getElementById('dynamic-fields-container'); // Corrected the ID here
    inputFieldsContainer.innerHTML = ''; // Clear previous fields

    while ((match = placeholderRegex.exec(templateContent)) !== null) {
        let inputField = createInputField(match[1]);
        inputFieldsContainer.appendChild(inputField);
    }
}

function createInputField(fieldName) {
    let container = document.createElement('div');
    let label = document.createElement('label');
    label.innerHTML = fieldName.charAt(0).toUpperCase() + fieldName.slice(1);
    let input = document.createElement('input');
    input.type = 'text';
    input.id = fieldName;
    input.name = fieldName;

    container.appendChild(label);
    container.appendChild(input);

    return container;
}

function sendEmail() {
    var templateId = document.getElementById("email-template").value;
    var subject = document.getElementById("email-subject").value;
    var toEmail = document.getElementById("email-to").value;
    var fromEmail = document.getElementById("email-from").value;
    var ccEmail = document.getElementById("email-cc").value;
    var templateContent = document.getElementById("template-preview").innerHTML;

    $.ajax({
        url: '/send_email/',
        type: 'post',
        headers: {'X-CSRFToken': getCSRF('csrftoken')},
        data: JSON.stringify({
            'subject': subject,
            'template_id': templateId,
            'template_content': templateContent,
            'to_email': toEmail,
            'from_email': fromEmail,
            'cc_email': ccEmail,
            'dynamic_fields': getDynamicFieldValues()
        }),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success: function(data) {
            alert(data.message);
        },
        error: function(xhr, errmsg, err) {
            alert('Failed to send email: ' + xhr.status + ": " + xhr.responseText);
        }
    });
}

function getDynamicFieldValues() {
    var dynamicFields = document.querySelectorAll('.dynamic-fields-content input[type="text"]');
    var fieldValues = {};

    dynamicFields.forEach(function(field) {
        fieldValues[field.id] = field.value;
    });

    return fieldValues;
}


function getCSRF(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.addEventListener('DOMContentLoaded', function() {
    updateTemplateAndSubject();
}, false);