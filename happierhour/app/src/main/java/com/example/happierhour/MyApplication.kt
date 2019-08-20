package com.example.happierhour

import android.app.Application

class MyApplication : Application() {
    companion object{
        var user_token = ""
        var filtered_hhs: String? = ""
        var bar_id: Int = 0
        var user = User_Model("","","","","")
        var review_id: Int = 0
        var myBarIds = ArrayList<Int>()
        var hh_id: Int = 0
    }

}