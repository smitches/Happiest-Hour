package com.example.happierhour

import org.json.JSONArray

class Bar_Model (id_input: Int, bar_name: String, street_address: String, phone_number: String, approved: Boolean,
                 manager: Int, region: Int, features: List<Int>) {

    var id: Int = id_input
    var bar_name: String = bar_name
    var street_address: String = street_address
    var phone_number: String = phone_number
    var manager_id: Int = manager
    var approved: Boolean = approved
    var region: Int = region
    var features: List<Int> = features


}

