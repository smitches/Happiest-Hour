package com.example.happierhour

class Bar_Model (bar_name: String, street_address: String, phone_number: String, approved: Boolean,
                 manager: User_Model, region: Int, features: List<Int>) {

    var bar_name: String = bar_name
    var street_address: String = street_address
    var phone_number: String = phone_number
    var manager: User_Model = manager
    var approved: Boolean = approved
    var region: Int = region
    var features: List<Int> = features
}

