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
  constructor(name, basis) {
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
    if (this.name) {
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
    var tex = String.raw`${this.number}\:\vphantom{\mathrm{${this.symetry.charAt(0)}}}^{${this.multiplicity}}\mathrm{${this.symetry}}`;
    return tex;
  };
}
class doi {
  constructor(doistring) {
    this.string = doistring
  };
  toString() {
    return this.string;
  };
  get url() {
    return 'https://doi.org/' + this.string;
  };
}

class excitationBase {
  constructor(initial, final) {
    this.initial = initial;
    this.final = final
  }
}
class excitationValue extends excitationBase {
  constructor(initial, final, value) {
    super(initial, final)
    this.value = value
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
    this.comment = null
    this.code = null
    this.method = null
    this.excitations = []
    this.DOI = null
  }
  static async loadAsync(file) {
    return this.loadString(await getTextFromFileAsync(getFullDataPath(file)));
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
        dat.DOI = new doi(value);
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
      var end = new state(parseInt(vals[3], 10), vals[4], vals[5]);
      var ex = new excitationValue(start, end, parseFloat(vals[6], 10));
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

class oneStateDataFile extends dataFileBase {
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
class AbsDataFile extends oneStateDataFile {

}
class FluoDataFile extends oneStateDataFile {

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