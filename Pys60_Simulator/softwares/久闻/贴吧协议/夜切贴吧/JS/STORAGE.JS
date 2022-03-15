function getDatabase() {
     return openDatabaseSync("tbclient", "1.0", "StorageDatabase", 10000000);
}

function initialize() {
    var db = getDatabase();
    db.transaction(
        function(tx) {
            tx.executeSql('CREATE TABLE IF NOT EXISTS settings(setting TEXT UNIQUE, value TEXT)');
            tx.executeSql('CREATE TABLE IF NOT EXISTS userInfo(userId TEXT UNIQUE, userName TEXT, BDUSS TEXT, password TEXT)');
            tx.executeSql('CREATE TABLE IF NOT EXISTS userCache(type TEXT UNIQUE, cache TEXT)');
            tx.executeSql('CREATE TABLE IF NOT EXISTS bookmark(threadId TEXT UNIQUE, postId TEXT, author TEXT, title TEXT, isLz BOOLEAN)');
          });
}

function setSetting(setting, value) {
   var db = getDatabase();
   var res = "";
   db.transaction(function(tx) {
        var rs = tx.executeSql('INSERT OR REPLACE INTO settings VALUES (?,?);', [setting,value]);
              if (rs.rowsAffected > 0) {
                res = "OK";
              } else {
                res = "Error";
              }
        }
  );
  return res;
}

function getSetting(setting) {
   var db = getDatabase();
   var res="";
   db.readTransaction(function(tx) {
     var rs = tx.executeSql('SELECT value FROM settings WHERE setting=?;', [setting]);
     if (rs.rows.length > 0) {
          res = rs.rows.item(0).value;
     } else {
         res = "Unknown";
     }
  })
  return res
}

function getSettingVal(setting, defaultVal) {
    var retVal = getSetting(setting)
    return (retVal == "Unknown" ? defaultVal : retVal)
}

function saveUserInfo(userId, userName, BDUSS, password){
    var db = getDatabase();
    var res = "";
    db.transaction(function(tx) {
        var rs = tx.executeSql('INSERT OR REPLACE INTO userinfo VALUES (?,?,?,?);', [userId, userName, BDUSS, password]);
               if (rs.rowsAffected > 0) {
                 res = "OK";
               } else {
                 res = "Error";
               }
         }
   );
   return res;
}

function getUserInfo(userId){
    var db = getDatabase()
    var res = []
    db.readTransaction(function(tx) {
                           if (userId==undefined){
                               var rs = tx.executeSql('SELECT * FROM userInfo')
                               for(var i = 0; i< rs.rows.length; i++)
                                   res.push({userId: rs.rows.item(i).userId,
                                                userName: rs.rows.item(i).userName,
                                                BDUSS: rs.rows.item(i).BDUSS,
                                                password: rs.rows.item(i).password})
                           } else {
                               var rs = tx.executeSql('SELECT * FROM userInfo WHERE userId=?;', [userId]);
                               if (rs.rows.length > 0)
                                   res.push({userId: rs.rows.item(0).userId,
                                                userName: rs.rows.item(0).userName,
                                                BDUSS: rs.rows.item(0).BDUSS,
                                                password: rs.rows.item(0).password})
                           }
                       })
    return res;
}

function deleteUserInfo(userId){
    var db = getDatabase();
            db.transaction(function(tx) {
                               if (userId==undefined)
                                   tx.executeSql('DELETE FROM userInfo')
                               else
                                   tx.executeSql('DELETE FROM userInfo WHERE userId =?;',[userId])
                           })
}

function setCache(type, cache){
    var db = getDatabase()
    var res = ""
    db.transaction(function(tx) {
         var rs = tx.executeSql('INSERT OR REPLACE INTO userCache VALUES (?,?);', [type, cache]);
               if (rs.rowsAffected > 0) {
                 res = "OK";
               } else {
                 res = "Error";
               }
         }
   );
   return res;
}
function getCache(type){
    var db = getDatabase();
    var res="";
    db.readTransaction(function(tx) {
      var rs = tx.executeSql('SELECT cache FROM userCache WHERE type=?;', [type]);
      if (rs.rows.length > 0) {
           res = rs.rows.item(0).cache;
      } else {
          res = "Unknown";
      }
   })
   return res
}
function clearCache(){
    var db = getDatabase();
    db.transaction(function(tx) {
                       tx.executeSql('DELETE FROM userCache')
                   })
}
function saveBookMark(threadId, postId, author, title, isLz){
    var db = getDatabase()
    var res = ""
    db.transaction(function(tx) {
         var rs = tx.executeSql('INSERT OR REPLACE INTO bookmark VALUES (?,?,?,?,?);',
                                [threadId, postId, author, title, isLz]);
               if (rs.rowsAffected > 0) {
                 res = "OK";
               } else {
                 res = "Error";
               }
         }
   );
   return res;
}
function getBookMark(listModel){
    var db = getDatabase()
    listModel.clear()
    db.readTransaction(function(tx) {
                           var rs = tx.executeSql('SELECT * FROM bookmark')
                           for (var i=0; i< rs.rows.length; i++)
                               listModel.append({
                                                    threadId: rs.rows.item(i).threadId,
                                                    postId: rs.rows.item(i).postId,
                                                    author: rs.rows.item(i).author,
                                                    title: rs.rows.item(i).title,
                                                    isLz: rs.rows.item(i).isLz
                                                })
                       })
}
function deleteBookMark(threadId){
    var db = getDatabase();
            db.transaction(function(tx) {
                               if (threadId==undefined)
                                   tx.executeSql('DELETE FROM bookmark')
                               else
                                   tx.executeSql('DELETE FROM bookmark WHERE threadId =?;',[threadId])
                           })
}
