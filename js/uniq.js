function uniq(array)
{
   if (array.length == 0) return [];
   const sortedArray = array.sort().map( x => [x, JSON.stringify(x)] );
   var uniqueArray = [ sortedArray[0][0] ];
   for (let i=1 ; i<sortedArray.length ; i++) {
     if ( sortedArray[i][1] != sortedArray[i-1][1])
       uniqueArray.push(sortedArray[i][0])
   }
   return uniqueArray;
}
