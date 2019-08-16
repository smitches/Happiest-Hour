package com.example.happierhour

class User_Model {

    var name: String? = null
    var email: String? = null
    var token: String? = null

    fun getNames(): String {
        return name.toString()
    }

    fun setNames(name: String) {
        this.name = name
    }

    fun getEmails(): String {
        return email.toString()
    }

    fun setEmails(name: String) {
        this.email = name
    }

}