package com.example.happierhour

import org.json.JSONArray
import org.json.JSONObject

class Bar_Model (val id_input: String, val bar_name: String, val street_address: String,val phone_number: String,
                 val approved: Boolean, manager: User_Model, region: Region_Model, features: ArrayList<Feature_Model>) {
}

class User_Model (val id_input: String, val username: String, val first_name: String,
                  val last_name: String,  val email: String){
}



class HH_Model (val hh_id: String, val hh_day: String, val hh_start_time: String,
                  val hh_end_time: String,  val hh_bar: Bar_Model, val hh_drinks:String,
                  val hh_food:String, val hh_menu : String){

}
class Review_Model(val r_id:String, val reviewer: User_Model, val bar: Bar_Model, val star_count: String, val review_text : String){}

class Region_Model(val reg_id:String, val reg_name:String){}

class Feature_Model(val f_id:String, val f_title:String, val f_desc:String){}

fun getRegionFromJSONObject(rJson:JSONObject) : Region_Model{
    return Region_Model(rJson.get("id").toString(),rJson.get("region_name").toString())
}

fun getFeatureFromJSONObject(rJson:JSONObject) : Feature_Model{
    return Feature_Model(rJson.get("id").toString(),rJson.get("feature_title").toString(),rJson.get("description").toString())
}

fun getHHFromJSONObject(hhJson:JSONObject) : HH_Model{
    val bar = getBarFromJSONObject(hhJson.getJSONObject("bar"))
    val hh = HH_Model(
        hhJson.get("id").toString(),
        hhJson.get("day_of_week").toString(),
        hhJson.get("start_time").toString(),
        hhJson.get("end_time").toString(),
        bar,
        hhJson.get("drinks").toString(),
        hhJson.get("food").toString(),
        hhJson.get("menu_pdf").toString()
        )
    return hh
}

fun getUserFromJSONObject(userJson:JSONObject) : User_Model{
    val user = User_Model(
        userJson.get("id").toString(),
        userJson.get("username").toString(),
        userJson.get("first_name").toString(),
        userJson.get("last_name").toString(),
        userJson.get("email").toString()
    )
    return user
}

fun getReviewFromJSONObject(reviewJson:JSONObject) : Review_Model{
    val review = Review_Model(
        reviewJson.get("id").toString(),
        getUserFromJSONObject(reviewJson.getJSONObject("reviewer")),
        getBarFromJSONObject(reviewJson.getJSONObject("bar")),
        reviewJson.get("star_count").toString(),
        reviewJson.get("review_text").toString()
    )
    return review
}

fun getBarFromJSONObject(barJson : JSONObject) : Bar_Model{
    val bar = Bar_Model(
        barJson.get("id").toString(),
        barJson.get("bar_name").toString(),
        barJson.get("street_address").toString(),
        barJson.get("phone_number").toString(),
        barJson.get("approved").toString() == "true" || barJson.get("approved").toString() == "True",
        getUserFromJSONObject(barJson.getJSONObject("manager")),
        getRegionFromJSONObject(barJson.getJSONObject("region")),
        getFeatureListFromJSONArray(barJson.getJSONArray("features"))
    )
    return bar
}

fun getFeatureListFromJSONArray(jsonArrayInput: JSONArray) : ArrayList<Feature_Model>{
    val size = jsonArrayInput.length()
    var featureList = ArrayList<Feature_Model>()
    for (i in 0 until size){
        val feature = getFeatureFromJSONObject(jsonArrayInput.getJSONObject(i))
        featureList.add(feature)
    }
    return featureList
}

fun getBarListFromJSONArray(jsonArrayInput:JSONArray): ArrayList<Bar_Model> {
    val size = jsonArrayInput.length()
    var barList = ArrayList<Bar_Model>()
    for (i in 0 until size){
        val barJson = jsonArrayInput.getJSONObject(i)
        val bar = getBarFromJSONObject(jsonArrayInput.getJSONObject(i))
        barList.add(bar)
    }
    return barList
}