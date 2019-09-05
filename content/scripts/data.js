class code {
  constructor(name,version){
    this.name=name;
    this.version=version;
  };
  toString() { 
    var str=this.name;
    if (this.version) {
      str=str+' ('+this.version+')';
    }
    return str;
  }
}
class basis {
  constructor(name,type){
    this.name=name;
    this.type=type;
  }
  toString() { 
    var str=this.name;
    if (this.type) {
      str=str+' ('+this.type+')';
    }
    return str;
  }
}

class state{
  constructor(number,multiplicity,symetry){
    this.number=number;
    this.multiplicity=multiplicity;
    this.symetry=symetry;
  };
  toString() { 
    var str=this.number+ ' ^'+this.multiplicity+this.symetry;
    return str;
  };
  toLaTeX() {
    var tex= String.raw`${this.number}\:\vphantom{\mathrm{${this.symetry.charAt(0)}}}^{${this.multiplicity}}\mathrm{${this.symetry}}`;
    return tex;
  };
}
class doi{
  constructor(doistring){
    this.string=doistring
  };
  toString() { 
    return this.string;
  };
  get url() {
    return 'https://doi.org/'+this.string;
  };
}
class excitation{
  constructor(start,end,Eabs){
    this.start=start;
    this.end=end;
    this.Eabs=Eabs;
  }
  toString() {
    return this.start+ ', ' + this.end +', '+ this.Eabs;
  }
}

class data {
  constructor(){
    this.title='';
    this.code=null;
    this.basis=null;
    this.doi=null;
    this.excitations=[];
  }
  static async loadAsync(file) {
    return new Promise(function (resolve, reject) {
    var req = new XMLHttpRequest();
    req.open("GET",getFullDataPath(file), true);
    req.onreadystatechange = function() {
      if (req.readyState == 4) {
        if (req.status == 200) {//when a good response is given do this
          var text = req.responseText;
          resolve(data.loadString(text));
        } else {
          reject({
            status: req.status,
            statusText: req.statusText
          });
        }
      }
    }
    req.send();
    });
  }
  static loadString(text) {
    // for each line with metadata
    var ismetaArea=true;
    //metadata RegExp (start with #; maybe somme spaces; : ; maybe somme space; datas)
    var meta=/^#\s*([A-Za-z]+)\s*:\s*(.*)$/;
    var dat=new data();
    function readmeta(line){
      // get key value
      var match=line.match(meta);
      // normalize key to lower
      var key=match[1].toLowerCase();
      //if data has value
      if(match.length==3 && match[2]) {
        var val=match[2];
        switch(key) {
          case "title":
            dat.title=val;
            break;
          case "code":
            var vals=val.split(",")
            if(vals.length>=2){
              dat.code=new code(vals[0],vals[1]);
            } else {
              dat.code=new code(vals[0],null);
            }
            break;
          case "basis":
            var vals=val.split(",")
            if(vals.length>=2){
              dat.basis=new basis(vals[0],vals[1])
            } else {
              dat.basis=new basis(vals[0],null);
            }
            break;
          case "doi":
            dat.doi=new doi(val);
            break;
        }
      }
    }
    function readrow(line){
      var vals=line.split(/\s+/);             
      var start=new state(parseInt(vals[0],10),parseInt(vals[1],10),vals[2]);
      var end=new state(parseInt(vals[3],10),vals[4],vals[5]);
      var ex=new excitation(start,end,parseFloat(vals[6],10));
      dat.excitations.push(ex);
    };

    text.split("\n").forEach(function(line) { 
      //if it's not empty line
      line=line.trim();
      if (line){
        //if # may be metadata or comment
        if (line.charAt(0)=="#") {
          //if it's metadata
          if(ismetaArea && meta.test(line)) {
            readmeta(line);
          }				
        } else { //else its row
          ismetaArea=false;
          readrow(line);
        }
      }
    });
    return dat
  }
}
