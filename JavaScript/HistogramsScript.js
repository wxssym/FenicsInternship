var inds = source.selected.indices;
const x = source.data['x'];
const y = source.data['y'];
hzeros=hzeros;
vzeros=vzeros;
hedges=hedges;
vedges=vedges;
if (inds.length === 0 || inds.length === x.length) 
{
    hh1.data_source.data["top"]  = hzeros;
    hh2.data_source.data["top"]  = hzeros;
    vh1.data_source.data["right"]  = vzeros;
    vh2.data_source.data["right"]  = vzeros;
} else {
    var neg_inds = new Array(x.length).fill(true);
    for (var i = 0; i < inds.length; i++) 
    {
        neg_inds[inds[i]] = false;
    }
    
    var hh1_selected = [];
    var vh1_selected = [];
    var hh2_selected = [];
    var vh2_selected = [];
    for (var i = 0; i < inds.length; i++) 
    {
    hh1_selected.push(x[inds[i]]);
    vh1_selected.push(y[inds[i]]);
    }
    for (var i = 0; i < neg_inds.length; i++) 
    {
    if (neg_inds[i]) {
        hh2_selected.push(x[i]);
        vh2_selected.push(y[i]);
    }
    hh1.data_source.data["top"]  = histogram(hh1_selected,hedges) ;
    vh1.data_source.data["top"]  = histogram(vh1_selected,vedges) ;
    hh2.data_source.data["right"]  = histogram(hh2_selected,hedges) ;
    vh2.data_source.data["right"]  = histogram(vh2_selected, vedges);
    }
}
console.log('selected')
console.log(hh1_selected)
console.log('unselected')
console.log(hh2_selected)
console.log('histogram bins selected')
console.log(hh1.data_source.data["top"])
console.log('histogram bins unselected')
console.log(hh1.data_source.data["top"])                

function histogram(data, bins) {
// Find the minimum and maximum values in the data
var minValue = Math.min(...data);
var maxValue = Math.max(...data);

// Calculate the width of each bin
var binWidth = (maxValue - minValue) / bins;

// Initialize an array to store the bin counts
var counts = new Array(bins).fill(0);

// Loop through the data and increment the appropriate bin count
for (var i = 0; i < data.length; i++) {
    var value = data[i];
    // Handle the edge case where the value is equal to the maximum value
    if (value === maxValue) {
    counts[bins - 1]++;
    } else {
    var binIndex = Math.floor((value - minValue) / binWidth);
    counts[binIndex]++;
    }
}

// Calculate the bin edges
var binEdges = new Array(bins + 1);
for (var i = 0; i <= bins; i++) {
    binEdges[i] = minValue + i * binWidth;
}

// Return the bin counts and bin edges as an object
return counts;
}

