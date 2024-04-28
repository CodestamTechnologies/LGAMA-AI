const fs = require('fs');
const XLSX = require('xlsx');
const { parse } = require('json2csv');

function excelToArray(file_path, sheet_name) {
    try {
        // Read the Excel file
        const workbook = XLSX.readFile(file_path);
        const sheet = workbook.Sheets[sheet_name];

        // Convert sheet to an array of objects
        const array_of_objects = XLSX.utils.sheet_to_json(sheet);

        return array_of_objects;
    } catch (error) {
        console.error(`Error: ${error.message}`);
        return null;
    }
}



function txtToArray(file_path) {
    try {
        // Read the TXT file
        const txtData = fs.readFileSync(file_path, 'utf-8');

        // Split the TXT data into lines
        const lines = txtData.trim().split('\n');

        // Initialize an array to hold the objects
        const array_of_objects = [];

        // Loop through each line
        lines.forEach((line, index) => {
            array_of_objects.push(line.trim());
        });

        return array_of_objects;
    } catch (error) {
        console.error(`Error: ${error.message}`);
        return null;
    }
}


function logErrorToCSV(email) {
    fs.access('error_log.csv', fs.constants.F_OK, (err) => {
        if (err) {
            // If the file doesn't exist, create one
            fs.writeFile('error_log.csv', '', (err) => {
                if (err) {
                    console.error('Error occurred while creating CSV file:', err);
                    return;
                }
                console.log('CSV file created successfully.');
                appendToCSV(email);
            });
        } else {
            // If the file exists, directly append to it
            appendToCSV(email);
        }
    });
}


function appendToCSV(email) {
    const csvFields = ['LeftEmails'];
    const csvOptions = { fields: csvFields, header: false };
    const csvData = parse({ 'LeftEmails': email }, csvOptions);

    // Append data to CSV file
    fs.appendFile('error_log.csv', csvData + '\n', (err) => {
        if (err) {
            console.error('Error occurred while appending to CSV file:', err);
        } else {
            console.log('Data appended to CSV file.');
        }
    });
}


module.exports = { txtToArray, excelToArray, logErrorToCSV };
