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
  static fromString(str) {
    var vals=str.split(",")
    if(vals.length>=2){
      return new code(vals[0],vals[1]);
    } else {
      return new code(vals[0],null);
    }
  }
}
class method {
  constructor(name,basis){
    this.name=name;
    this.basis=basis;
  }
  static fromString(str) {
    var vals=str.split(",")            
    return new method(vals[0],vals[1]);
  }
  toString() { 
    var str=this.name;
    if (this.name) {
      str=str+'/'+this.basis;
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
  constructor(start,end,Eabs,Efluo,EZPE){
    this.start=start;
    this.end=end;
    this.Eabs=Eabs;
    this.Efluo=Efluo;
    this.EZPE=EZPE;
  }
  get Ezz() {
     return this.Eabs-this.Efluo+this.EZPE
  }
  toString() {
    return this.start+ ', ' + this.end +', '+ this.Eabs.toPrecision(3);
  }
}

class CalcParams {
  constructor(){
    this.code=null;
    this.method=null;
  }
}
class StateCalcParams extends CalcParams {
  constructor(){
    super()
    this.geometry;
  }
}

class data {
  constructor(){
    this.molecule='';
    this.comment;
    this.GS=new StateCalcParams();
    this.ES=new StateCalcParams();
    this.ZPE=new CalcParams();
    this.doi=null;
    this.excitations=[];
  }
  static async loadAsync(file) {
   return data.loadString(await getTextFromFileAsync(getFullDataPath(file)));
  }
  static loadString(text) {
    // for each line with metadata
    var ismetaArea=true;
    //metadata RegExp (start with #; maybe somme spaces; : ; maybe somme space; datas)
    var meta=/^#\s*([A-Za-z_]+)\s*:\s*(.*)$/;
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
          case "molecule":
            dat.molecule=val
            break;
          case "comment":
            dat.comment=val
            break;
          case "gs_code":
            dat.GS.code=code.fromString(val)
            break;
          case "gs_method":
            dat.GS.method=method.fromString(val)
            break;
          case "gs_geom":
            dat.GS.geometry=method.fromString(val)
            break;
          case "es_code":
            dat.ES.code=code.fromString(val)
            break
          case "es_method":
            dat.ES.method=method.fromString(val)
            break;
          case "es_geom":
            dat.ES.geometry=method.fromString(val)
            break;
          case "zpe_code":
            dat.ZPE.code=code.fromString(val)
            break
          case "zpe_method":
            dat.ZPE.method=method.fromString(val)
            break;         
          case "doi":
            dat.doi=new doi(val);
            break;
        }
      }
    }
    function readrow(line){
      var vals=line.split(/\s+/);
      while (vals.length<8){
        vals.push(null);
      }
      var start=new state(parseInt(vals[0],10),parseInt(vals[1],10),vals[2]);
      var end=new state(parseInt(vals[3],10),vals[4],vals[5]);
      var ex=new excitation(start,end,parseFloat(vals[6],10),parseFloat(vals[7],10),parseFloat(vals[8],10));
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
