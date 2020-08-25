document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('','','',''));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipient, subject, time, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-read').style.display = 'none';

  // Clear out composition fields or preset to reply
  var presetSubject = "";
  if(subject != ""){
    presetSubject = "Re: ".concat(subject)
    document.querySelector('#compose-recipients').value = recipient;
    document.querySelector('#compose-subject').value = presetSubject;
    document.querySelector('#compose-body').value = 
    `On ${time} ${recipient} wrote:
    
    ${body}`;
  } else {
    // Not replying
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  document.querySelector('#compose-form').onsubmit = () => {
    const c_recipient = document.querySelector('#compose-recipients').value;
    const c_subject = document.querySelector('#compose-subject').value;
    const c_body = document.querySelector('#compose-body').value;
    console.log(c_recipient);
    console.log(c_subject);
    console.log(c_body);

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: c_recipient,
          subject: c_subject,
          body: c_body,
          read: false
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        if(result.message === "Email sent successfully.")
        {
          load_mailbox('sent');
        }
    });
    return false;
  }
}

var selectedMails = [];
//Handle Archives

function archiveSelected(mailbox) {
  if(selectedMails.length > 0)
  {
    for(i=0;i<selectedMails.length;i++){
      var taskDone = false;
      if(i === selectedMails.length-1) taskDone = true;
      fetch(`/emails/${selectedMails[i]}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      .then(() => {
        if(taskDone) load_mailbox('inbox');
      });
    }
    
  } 
}

function unarchiveSelected(mailbox) {
  if(selectedMails.length > 0) {
    for(i=0;i<selectedMails.length;i++){
      var taskDone = false;
      if(i === selectedMails.length-1) taskDone = true;
      fetch(`/emails/${selectedMails[i]}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      .then(() => {
        if(taskDone) load_mailbox('inbox');
      });
    }
  }
  
}

function setTopButton(mailbox) {
  var topButtonHolder = document.querySelector('#topbuttongroup');
  topButtonHolder.innerHTML= "";

  //button1
  button1 = document.createElement('button');
  button1.className += "btn btn-secondary TopButtons";
  button1.id = "archive_email";
  button1.innerText = "Archive Selected";
  button1.addEventListener('click', () => archiveSelected());
  topButtonHolder.appendChild(button1);

  //button1
  button2 = document.createElement('button');
  button2.className += "btn btn-secondary TopButtons";
  button2.id = "unarchive_email";
  button2.innerText = "Unarchive Selected";
  button2.addEventListener('click', () => unarchiveSelected());
  topButtonHolder.appendChild(button2);
  
}

function load_mailbox(mailbox) {
  //Clear out email selection
  selectedMails = [];
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-read').style.display = 'none';

  // Show the mailbox name
  const mailViewName = document.querySelector('#mailboxname');
  mailViewName.innerText = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;

  setTopButton(mailbox);

  document.querySelector('#email-listgroup').innerHTML = "";
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    for(var i = 0; i < emails.length; i++) {
      var email = emails[i];
      var newmail = document.createElement('ul');
      
      newmail.innerHTML = `<li class="list-group-item checkboxarea"><input type="checkbox" id="archive_${email.id}"></li>`;
      newmail.className = "list-group list-group-horizontal";

      const newmailInside = document.createElement('li');
      newmailInside.innerHTML = `<b class="mailsender">${email.sender}</b> <p class="mailtitle" >${email.subject}</p> <p class="timestamp">${email.timestamp}</p>`;
      newmailInside.id=`mail${email.id}`;

      if(email.read === true){
        newmailInside.className = "list-group-item readmailcontainer";
      }
      else{
        newmailInside.className = "list-group-item mailcontainer";
      }
      //Add Email View
      var mailid = email.id;
      newmailInside.addEventListener('click', function() {
        document.querySelector('#emails-read').style.display = 'block';
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        
        id = this.id.slice(4);
        fetch(`/emails/${id}`)
        .then(response => response.json())
        .then(email => {
          // Print email
          console.log(email);
          document.querySelector('#viewtitle').innerHTML = `${email.subject}`;
          document.querySelector('#viewcontent').innerHTML = `${email.body}`;
          document.querySelector('#viewauthor').innerHTML = `By: ${email.sender}`;
          document.querySelector('#viewtimestamp').innerHTML = `Timestamp: ${email.timestamp}`;
          document.querySelector('#replyButton').addEventListener('click', () => compose_email(`${email.sender}`,`${email.subject}`,`${email.timestamp}`,`${email.body}`));
      
          var recipients = "";
          for(i=0;i<email.recipients.length;i++)
          {
            recipients = recipients.concat(`${email.recipients[i]} `);
          }
          document.querySelector('#viewrecipient').innerHTML = `To: ${recipients}`;
        });
        }
      );

      newmail.appendChild(newmailInside);
      document.querySelector('#email-listgroup').appendChild(newmail);
      //checkbox event
      document.querySelector(`#archive_${email.id}`).addEventListener('change', function() {
        arrayid = this.id.slice(8);
        if(this.checked){
          //select item
          selectedMails[selectedMails.length] = arrayid;
        } 
        else {
          //deselect item
          for(var i = 0; i < selectedMails.length; i++)
          {
            if(selectedMails[i] === arrayid)
            {
              selectedMails.splice(i,1);
            }
          }
        }
        console.log(selectedMails);
      });
    }
    // ... do something else with emails ...
  });
}

