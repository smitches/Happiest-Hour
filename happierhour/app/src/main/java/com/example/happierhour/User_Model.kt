package com.example.happierhour


class User_Model (val id: Int, val username: String, val first_name: String,
                  val last_name: String,  val email: String){

    var mytoken: String? = null

    fun getTokens(): String {
        return mytoken.toString()
    }

    fun setTokens(name: String) {
        this.mytoken = name
    }

}
