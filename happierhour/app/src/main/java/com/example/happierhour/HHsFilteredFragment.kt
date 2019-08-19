package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.hhs_filtered.*
import org.json.JSONArray
import com.example.happierhour.MyApplication.Companion.filtered_hhs

class HHsFilteredFragment() : Fragment() {

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {

        println(filtered_hhs)
        val view = inflater.inflate(R.layout.hhs_filtered, container, false)

        var adapter : MyHHAdapter? = null
        var hhList : ArrayList<HH_Model>
        hhList = generateHappyHourData()

        adapter = MyHHAdapter(requireActivity(), hhList)

        println(adapter == null)

        hh_list.adapter = adapter

//        list.setOnItemClickListener { adapterView, view, i, l ->
//            Toast.makeText(this, "Selected Emp is = "+ hhList.get(i).emp_name, Toast.LENGTH_SHORT).show()
//        }
        return view
    }

    private fun generateHappyHourData(): ArrayList<HH_Model> {
        var result = ArrayList<HH_Model>()

        val hhs_to_list = JSONArray(filtered_hhs)

        for (i in 0..(hhs_to_list.length() - 1)) {
            val happyHour = hhs_to_list.getJSONObject(i)
            var hh: HH_Model = HH_Model()
            hh.hh_id = happyHour.get("id").toString().toInt()
            hh.hh_day = happyHour.get("day_of_week").toString()
            hh.hh_start_time = happyHour.get("start_time").toString()
            hh.hh_end_time = happyHour.get("end_time").toString()
            var bar = happyHour.getJSONObject("bar")
            hh.hh_bar = bar.get("bar_name").toString()
            hh.hh_drinks = happyHour.get("drinks").toString()
            hh.hh_food = happyHour.get("food").toString()
            hh.hh_menu = happyHour.get("menu_pdf").toString()

            result.add(hh)
        }

        filtered_hhs = ""

        return result
    }

}
