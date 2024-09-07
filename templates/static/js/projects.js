document.getElementById('whatsappForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const number = document.getElementById('number').value;
    const message = document.getElementById('message').value;
    const time_hour = document.getElementById('timeHour').value;
    const time_minute = document.getElementById('timeMinute').value;

    fetch('/send_whatsapp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ number, message, time_hour, time_minute }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('smsForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const number = document.getElementById('smsNumber').value;
    const message = document.getElementById('smsMessage').value;

    fetch('/send_sms', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ number, message }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('callForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const number = document.getElementById('callNumber').value;

    fetch('/make_call', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ number }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('emailForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const receiver_email = document.getElementById('receiverEmail').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    fetch('/send_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ receiver_email, subject, body }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('scrapeForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const query = document.getElementById('query').value;

    fetch('/scrape_top_results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('scrapeResults').innerText = JSON.stringify(data.results, null, 2);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('scheduleEmailForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const receiver_email = document.getElementById('scheduleReceiverEmail').value;
    const subject = document.getElementById('scheduleSubject').value;
    const body = document.getElementById('scheduleBody').value;
    const send_time = document.getElementById('sendTime').value;

    fetch('/schedule_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ receiver_email, subject, body, send_time }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('emailWithAttachmentForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const receiver_email = document.getElementById('attachmentReceiverEmail').value;
    const subject = document.getElementById('attachmentSubject').value;
    const body = document.getElementById('attachmentBody').value;
    const attachment_path = document.getElementById('attachmentPath').value;

    fetch('/send_email_with_attachment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ receiver_email, subject, body, attachment_path }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('runTrainButton').addEventListener('click', function () {
    fetch('/run_train_command', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('liveVideoButton').addEventListener('click', function () {
    fetch('/live_video_streaming', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('printTableForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const data = document.getElementById('tableData').value;

    fetch('/print_table', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: JSON.parse(data) }),
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById('tableOutput').innerText = data;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('rainbowForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const text = document.getElementById('rainbowText').value;

    fetch('/rainbow_terminal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById('rainbowOutput').innerText = data;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('collegeSearchForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const college_name = document.getElementById('collegeName').value;

    fetch('/search_by_college', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ college_name }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('collegeSearchOutput').innerText = JSON.stringify(data.students, null, 2);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.getElementById('displayTeamButton').addEventListener('click', function () {
    fetch('/display_team_data', {
        method: 'GET',
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById('teamDataOutput').innerText = data;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
