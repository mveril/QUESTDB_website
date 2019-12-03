class excitationType {
  static get VALENCE(){return 1}
  static get RYDBERG(){return 2}
  static get PiPis(){return 4}
  static get nPis(){return 8}
  static get Singulet(){return 16}
  static get Doublet(){return 32}
}
class code {
  constructor(name, version) {
    this.name = name;
    this.version = version;
  };
  toString() {
    var str = this.name;
    if (this.version) {
      str = str + ' (' + this.version + ')';
    }
    return str;
  }
  static fromString(str) {
    var vals = str.split(",")
    if (vals.length >= 2) {
      return new code(vals[0], vals[1]);
    } else {
      return new code(vals[0], null);
    }
  }
}
class method {
  constructor(name, basis=null) {
    this.name = name;
    this.basis = basis;
  }
  static fromString(str) {
    var vals = str.split(",")
    if (vals.length == 2) {
      return new method(vals[0], vals[1]);
    }
    else {
      return new method(vals[0], null)
    }
  }
  toString() {
    var str = this.name;
    if (this.basis) {
      str = str + '/' + this.basis;
    }
    return str;
  }
}

class state {
  constructor(number, multiplicity, symetry) {
    this.number = number;
    this.multiplicity = multiplicity;
    this.symetry = symetry;
  };
  toString() {
    var str = this.number + ' ^' + this.multiplicity + this.symetry;
    return str;
  };
  toLaTeX() {
    var tex = String.raw`${this.number}\:^{${this.multiplicity}}\mathrm{${this.symetry}}`;
    return tex;
  };
}
class DOI {
  constructor(doistring) {
    this.string = doistring
  };
  toString() {
    return this.string;
  };
  get url() {
    return new URL(this.string,'https://doi.org').toString()
  }
}

class excitationBase {
  constructor(initial, final, type=null, T1=null) {
    this.initial = initial;
    this.final = final
    if (type !== null) {
      tys = type.split(";")
      const arrow = String.raw('\rightarrow')
      for (ty in tys) {
        if (ty.include(arrow)) {
          initial, final = ty.split(arrow, 2)
          initials = initial.split(",")
          if (initials.length==2||initials.length==2){
            trty = trty| excitationType.Singulet
          }
          else{
            trty = trty | excitationType.Doublet
          }
          finals = final.split(",").map(x => x.strip())
          if (initials.include("n") && finals.include(String.raw('\pis'))) {
            trty = trty | excitationType.PiPis
          } else if (initials.include(String.raw('\pi')) in initials && finals.include(String.raw('\pis'))) {
            trty = trty | excitationType.PiPis
          } else if (ty.include(String.raw('\Ryd'))) {
            trty = trty | excitationType.RYDBERG
          } else if (ty.include(String.raw('\Val'))) {
            trty = trty | excitationType.VALENCE
          }
        }
      }
    }
    this.T1 = T1
  }
}
class excitationValue extends excitationBase {
  constructor(initial, final, type, value,corrected=null,oscilatorForces=null,T1=null) {
    super(initial, final, type, T1=null)
    this.value = value
    this.corrected = corrected
    this.oscilatorForces = oscilatorForces
  }
}

class excitation extends excitationBase {
  constructor(initial, final, Eabs, Efluo, EZPE) {
    super(initial, final)
    this.Eabs = Eabs
    this.Efluo = Efluo
    this.EZPE = EZPE
  }
  get Eadia() {
    return (this.Eabs + this.Efluo) / 2
  }
  get Ezz() {
    return this.Eadia - this.EZPE
  }
  toString() {
    return this.start + ', ' + this.end + ', ' + noNanPrecision(this.Eabs, 3);
  }
}

class dataFileBase {
  constructor() {
    this.molecule = ''
    this.comment = ""
    this.code = null
    this.method = null
    this.excitations = []
    this.DOI = null
    this.sourceFile=null
  }
  get isTBE(){
    return this.method.name="TBE"
  }
  static async loadAsync(file) {
    switch (trueTypeOf(file)) {
      case String.name:
        file=getFullDataPath(file)
        var str=await getTextFromFileUrlAsync(file)
        break;
      case File.name:
        var str=await getTextFromUploadedFileAsync(file)
        break
    }
    var dat = this.loadString(str);
    dat.sourceFile=new websiteFile(file)
    return dat
  }
  static readmetaPair(key, value, dat) {
    switch (key) {
      case "molecule":
        dat.molecule = value
        break;
      case "comment":
        dat.comment = value
        break;
      case "code":
        dat.code = code.fromString(value)
        break;
      case "method":
        dat.method = method.fromString(value)
        break;
      case "doi":
        dat.DOI = new DOI(value);
        break;
      default:
    }
  }
  static loadString(text) {
    // for each line with metadata
    var ismetaArea = true;
    //metadata RegExp (start with #; maybe somme spaces; : ; maybe somme space; datas)
    var meta = /^#\s*([A-Za-z_]+)\s*:\s*(.*)$/;
    var classname = this.name
    var dat = eval(String.raw`new ${this.name}()`)
    function readmeta(line) {
      // get key value
      var match = line.match(meta)
      // normalize key to lower
      var key = match[1].toLowerCase()
      //if data has value
      if (match.length == 3 && match[2]) {
        var val = match[2]
        eval(String.raw`${classname}.readmetaPair(key,val,dat)`)
      }
    }
    function readrow(line) {
      var vals = line.split(/\s+/);
      while (vals.length < 8) {
        vals.push(null);
      }

      var start = new state(parseInt(vals[0], 10), parseInt(vals[1], 10), vals[2]);
      var end = new state(parseInt(vals[3], 10), parseInt(vals[4],10), vals[5]);
      var hasType=vals.length>=7 && parseFloat(vals[6],10)==NaN
      var type=((vals.length>=7 && hasType) ? vals[6] : null)
      var val=((vals.length>=7+hasType) ? parseFloat(vals[6+hasType], 10): NaN)
      var cor=((vals.length>=8+hasType) ? parseFloat(vals[7+hasType], 10): NaN)
      var oscilatorForces=((vals.length>=9+hasType) ? parseFloat(vals[8+hasType],10): NaN)
      var T1=((vals.length>=10+hasType) ? parseFloat(vals[9+hasType],10): NaN)
      var ex = new excitationValue(start, end, type, val,cor,oscilatorForces,T1);
      dat.excitations.push(ex);
    };

    for (var line of text.split("\n")) {
      //if it's not empty line
      line = line.trim();
      if (line) {
        //if # may be metadata or comment
        if (line.charAt(0) == "#") {
          //if it's metadata
          if (ismetaArea && meta.test(line)) {
            readmeta(line);
          }
        } else { //else its row
          ismetaArea = false;
          readrow(line);
        }
      }
    }
    return dat
  }
}

class oneStateDataFileBase extends dataFileBase {
  constructor() {
    super()
    this.geometry = null
  }
  static readmetaPair(key, value, dat) {
    if (key == "geom") {
      dat.geometry = method.fromString(value)
    }
    else {
      dataFileBase.readmetaPair(key, value, dat)
    }
  }
}
class AbsDataFile extends oneStateDataFileBase {

}
class FluoDataFile extends oneStateDataFileBase {

}
class twoStateDataFileBase extends dataFileBase {
  constructor() {
    super()
    this.GS = null
    this.ES = null
  }
  static readmetaPair(key, value, dat) {
    switch (key) {
      case "gs":
        dat.GS = method.fromString(value)
        break;
      case "es":
        dat.ES = method.fromString(value)
        break;
      default:
        dataFileBase.readmetaPair(key, value, dat)
    }
  }
}
class ZPEDataFile extends twoStateDataFileBase {

}
class CombinedData {
  constructor() {
    this.Abs = null
    this.Fluo = null
    this.ZPE = null
  }
  get excitations() {
    var exs = []
    var dic = new Map()
    if (this.Abs != null) {
      for (const el of this.Abs.excitations) {
        var key = JSON.stringify([el.initial, el.final])
        if (!dic.has(key)) {
          dic.set(key, {})
        }
        dic.get(key)["abs"] = el.value
      }
      if (this.Fluo != null) {
        for (const el of this.Fluo.excitations) {
          var key = JSON.stringify([el.initial, el.final])
          if (!dic.has(key)) {
            dic.set(key, {})
          }
          dic.get(key)["fluo"] = el.value
        }
      }
      if (this.ZPE != null) {
        for (const el of this.ZPE.excitations) {
          var key = JSON.stringify([el.initial, el.final])
          if (!dic.has(key)) {
            dic.set(key, {})
          }
          dic.get(key)["ZPE"] = el.value
        }
      }
      dic.forEach((value, key) => {
        var eabs = NaN
        var efluo = NaN
        var eZPE = NaN
        var mykey = JSON.parse(key)
        for (var el of mykey) {
          Reflect.setPrototypeOf(el, state.prototype)
        }
        if ("abs" in value) {
          eabs = value["abs"]
        }
        if ("fluo" in value) {
          efluo = value["fluo"]
        }
        if ("ZPE" in value) {
          eZPE = value["ZPE"]
        }
        exs.push(new excitation(mykey[0], mykey[1], eabs, efluo, eZPE))
      })
      return exs
    }
  }
}