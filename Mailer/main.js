const { SendMail } = require('./index');
const { txtToArray } = require('./excelToArray');

const path = require('path'); // Import the path module

async function sendEmails(file_name) {
    try {
        // Read data from the text file
        const data = txtToArray(path.join('..', file_name));

        // Function to send a single email with a delay
        const sendEmailWithDelay = async (email) => {
            const username = email.toString().split('@')[0];
            await new Promise((resolve) => {
                setTimeout(async () => {
                    try {
                        await SendMail(email, email, username);
                        console.log(email + ' has been sent an email!');
                        resolve();
                    } catch (error) {
                        resolve(error);
                    }
                }, 1000); // Change delay time as needed (1000 ms = 1 second)
            });
        };

        // Create an array of promises for sending emails with delay
        const emailPromises = data.map((email) => sendEmailWithDelay(email));

        // Wait for all email promises to resolve
        await Promise.all(emailPromises);
        console.log('All emails sent successfully');
    } catch (error) {
        console.error('Error sending emails:', error);
    }
}

// Pass the file name as a command line argument to the function
sendEmails(process.argv[2]);
