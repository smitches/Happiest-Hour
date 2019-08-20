package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.bar_id
import kotlinx.android.synthetic.main.add_bar.*
import kotlinx.android.synthetic.main.add_bar.view.*
import kotlinx.android.synthetic.main.add_hh.*
import kotlinx.android.synthetic.main.filter_hhs.*
import kotlinx.android.synthetic.main.filter_hhs.SpinnerDay
import kotlinx.android.synthetic.main.filter_hhs.checkDrink
import kotlinx.android.synthetic.main.filter_hhs.checkFood
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import org.json.JSONArray

class AddHHFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.add_hh, container, false)

        view.button.setOnClickListener {

            val selectedDay: String = SpinnerDay.selectedItem.toString()
            val startTimeInput: String = startTimeEdit.text.toString()
            val endTimeInput: String = endTimeEdit.text.toString()

            val drinksInput: Boolean = checkDrink.isChecked()
            val foodInput: Boolean = checkFood.isChecked()
            val menuInput: String = menuPDFEdit.text.toString()

            val contents: HashMap<String, String> = HashMap<String, String>()

            if (selectedDay != "") {
                var dayString: String = ""
                if (selectedDay == "Monday") {
                    dayString = "M"
                } else if (selectedDay == "Tuesday") {
                    dayString = "T"
                } else if (selectedDay == "Wednesday") {
                    dayString = "W"
                } else if (selectedDay == "Thursday") {
                    dayString = "Th"
                } else if (selectedDay == "Friday") {
                    dayString = "F"
                } else if (selectedDay == "Saturday") {
                    dayString = "Sa"
                } else if (selectedDay == "Tuesday") {
                    dayString = "Su"
                }
                contents.put("day_of_week", dayString)
            }

            contents.put("start_time", startTimeInput)
            contents.put("end_time", endTimeInput)

            if (drinksInput == true) {
                contents.put("drinks", "true")
            } else {
                contents.put("drinks", "false")
            }

            if (foodInput == true) {
                contents.put("food", "true")
            } else {
                contents.put("food", "false")
            }

            contents.put("menu_pdf", menuInput)

            doAsync {

                println(contents)
                val postresponse = addInfo(contents)
                println(postresponse)

            }

            (activity as NavigationHost).navigateTo(ManageBarsFragment(), addToBackstack = false)

        }

        return view
    }

    private fun addInfo(contents: HashMap<String, String>): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://http://happierhour.appspot.com/api/bar/$bar_id/happyhours/create"

        val response_body = request.POST(url, contents)

        println(response_body)

        return response_body

    }
}
