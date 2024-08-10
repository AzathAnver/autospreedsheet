function exportSpreadsheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var url = "https://docs.google.com/spreadsheets/d/" + spreadsheet.getId() + "/export?format=xlsx";
  var options = {
    headers: {
      Authorization: 'Bearer ' + ScriptApp.getOAuthToken()
    },
    muteHttpExceptions: true
  };
  
  var response = UrlFetchApp.fetch(url, options);
  var fileName = spreadsheet.getName() + ".xlsx";
  var folder = DriveApp.getFolderById("1A2B3C4D5E6F7G8H9I0J"); // Replace with your Folder ID
  folder.createFile(response.getBlob()).setName(fileName);
}