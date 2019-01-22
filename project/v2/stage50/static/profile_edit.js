// Execute when the DOM is fully loaded
$(document).ready(function() {

    preselectRadioButton();

    // Configure typeahead
    configureTypeahead();




});


function configureTypeahead() {
    $("#locationString").typeahead({
        highlight: true,
        minLength: 1
    },
    {
        display: function(suggestion) { return null; },
        limit: 10,
        source: lookup,
        templates: {
            suggestion: Handlebars.compile(
                "<div class='suggestion-box'>" +
                "{{ matching_full_name }}" +
                "</div>"
            )
        }
    });

    // Fill form fields after place is selected from drop-down
    $("#locationString").on("typeahead:select", function(eventObject, suggestion, name) {
        $("#country").val(suggestion.country);
        $("#state").val(suggestion.admin1);
        $("#city").val(suggestion.city);
        $("#geoname_id").val(suggestion.geoname_id);
        $("#full_name").val(suggestion.full_name);
        $("#country_isoalpha2").val(suggestion.country_isoalpha2);
        $("#country_isoalpha3").val(suggestion.country_isoalpha3);
        $("#admin1_code").val(suggestion.admin1_code);
        $("#latitude").val(suggestion.latitude);
        $("#longitude").val(suggestion.longitude);
    });

}


// Search database for typeahead's suggestions
function lookup(query, syncResults, asyncResults)
{
    // Get places matching query (asynchronously)
    let parameters = {
        locationString: query
    };
    $.getJSON("/lookup", parameters, function(data, textStatus, jqXHR) {

        // Call typeahead's callback with search results (i.e., places)
        asyncResults(data);
    });
}


function preselectRadioButton() {
    // Get all gender radio inputs in an array
    var genderRadioButtons = Array.from($("[name='gender']"));

    genderRadioButtons.forEach(function(radioButton){
        radioButton.checked = (radioButton.value == user.gender);
    });
}
