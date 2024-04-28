const dotenv = require('dotenv');
const path = require('path');

// Load environment variables from .env file in project_directory
dotenv.config({ path: path.resolve(__dirname, '../.env') });

// The rest of your code remains unchanged
const nodemailer = require('nodemailer');
const { logErrorToCSV } = require('./excelToArray');

const transporter = nodemailer.createTransport({
  host: 'smtp.hostinger.com',
  port: 587,
  secure: false,
  auth: {
    user: process.env.SMTP_USERNAME,
    pass: process.env.SMTP_PASSWORD,
  },
  pool: true,
});

const options = (email, fullname, username) => ({
  from: process.env.SMTP_USERNAME,
  to: email,
  subject: "Is it the right time ?",
  html: `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
  <html dir="ltr" lang="en">
  
    <head>
      <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    </head>
    <div style="display:none;overflow:hidden;line-height:1px;opacity:0;max-height:0;max-width:0">Join Us at Codestam Technologies<div> ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿ ‌​‍‎‏﻿</div>
    </div>
  
    <body style="background-color:rgb(255,255,255);margin-top:auto;margin-bottom:auto;margin-left:auto;margin-right:auto;font-family:ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;;padding-left:0.5rem;padding-right:0.5rem">
      <table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation" style="max-width:465px;border-width:1px;border-style:solid;border-color:rgb(234,234,234);border-radius:0.25rem;margin-top:40px;margin-bottom:40px;margin-left:auto;margin-right:auto;padding:20px">
        <tbody>
          <tr style="width:100%">
            <td>
              <table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation" style="margin-top:32px">
                <tbody>
                  <tr>
                    <td><img alt="Codestam technologies" src="https://github.com/Souravvmishra/photos/raw/master/logo.webp" style="display:block;outline:none;border:none;text-decoration:none;margin-top:0px;margin-bottom:0px;margin-left:auto;margin-right:auto;width:7rem" /></td>
                  </tr>
                </tbody>
              </table>
              <p style="font-size:14px;line-height:24px;margin:16px 0;color:rgb(0,0,0)">Hello 
              <!-- -->${fullname}<!-- -->,
              </p>
              <p style="font-size:14px;line-height:24px;margin:16px 0;color:rgb(0,0,0)">
              <strong>${username}</strong>
              , <!-- --> <!-- -->Do you think this is the right time to get a <strong>Website </strong>for your <strong>business?<strong/></p>
              <table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation">
                <tbody>
                  <tr>
                    <td>
                      <table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation">
                        <tbody style="width:100%">
                          <tr style="width:100%">
                            <td align="right" data-id="__react-email-column"><img height="64" src="https://github.com/Souravvmishra/photos/raw/master/offline02.webp" style="display:block;outline:none;border:none;text-decoration:none;border-radius:9999px" width="64" /></td>
                            <td align="center" data-id="__react-email-column"><img alt="invited you to" height="9" src="https://github.com/Souravvmishra/photos/raw/master/vercel-arrow.webp" style="display:block;outline:none;border:none;text-decoration:none" width="12" /></td>
                            <td align="left" data-id="__react-email-column"><img height="64" src="https://github.com/Souravvmishra/photos/raw/master/image.webp" style="display:block;outline:none;border:none;text-decoration:none;border-radius:9999px" width="64" /></td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation" style="text-align:center;margin-top:32px;margin-bottom:32px">
                <tbody>
                  <tr>
                    <td><a href="https://api.whatsapp.com/send?phone=918797969991&amp;text=Hi%20Codestam" style="line-height:100%;text-decoration:none;display:inline-block;max-width:100%;background-color:rgb(0,0,0);border-radius:0.25rem;color:rgb(255,255,255);font-size:12px;font-weight:600;text-decoration-line:none;text-align:center;padding-left:1.25rem;padding-right:1.25rem;padding-top:0.75rem;padding-bottom:0.75rem;padding:12px 20px 12px 20px" target="_blank"><span><!--[if mso]><i style="letter-spacing: 20px;mso-font-width:-100%;mso-text-raise:18" hidden>&nbsp;</i><![endif]--></span><span style="max-width:100%;display:inline-block;line-height:120%;mso-padding-alt:0px;mso-text-raise:9px">Yes</span><span><!--[if mso]><i style="letter-spacing: 20px;mso-font-width:-100%" hidden>&nbsp;</i><![endif]--></span></a></td>
                  </tr>
                </tbody>
              </table>
              <p style="font-size:14px;line-height:24px;margin:16px 0;color:rgb(0,0,0)">Website :<!-- --> <a href="https://codestam.com" style="color:rgb(37,99,235);text-decoration:none;text-decoration-line:none" target="_blank">https://codestam.com</a> <br />Phone :<!-- --> <a href="tel:+918797969991" style="color:rgb(37,99,235);text-decoration:none;text-decoration-line:none" target="_blank">+91 87979 69991</a><br />Codestam Store :<!-- --> <a href="https://store.codestam.com/" style="color:rgb(37,99,235);text-decoration:none;text-decoration-line:none" target="_blank">Codestam Store</a>
              <a href="mailto:kushwaha@codestam.com" style="color:rgb(37,99,235);text-decoration:none;text-decoration-line:none" target="_blank">Mail Us at:</a>
              </p>
              <hr style="width:100%;border:none;border-top:1px solid #eaeaea;border-width:1px;border-style:solid;border-color:rgb(234,234,234);margin-top:26px;margin-bottom:26px;margin-left:0px;margin-right:0px" />
              <p style="font-size:12px;line-height:24px;margin:16px 0;color:rgb(102,102,102)">This invitation was intended for<!-- --> <span style="color:rgb(0,0,0)">
              ${fullname}
              </span>. If you were not expecting this invitation, you can ignore this email.</p>
            </td>
          </tr>
        </tbody>
      </table>
    </body>
  
  </html>`,
});

function SendMail(email, fullname, name) {
  return new Promise((resolve, reject) => {
    const mailOptions = options(email, fullname, name);
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.error(`Error occurred while sending Email: ${error}`);
        // Log error to CSV file
        logErrorToCSV(email);
        reject(false);
      } else {
        console.log('Email sent:', info.response);
        resolve(true);
      }
    });
  });
}

module.exports = { SendMail }
