package com.example.happierhour

import android.app.Activity
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView

class MyHHAdapter (private var activity: Activity, private var items: ArrayList<HH_Model>) :  BaseAdapter(){

    private class ViewHolder(row: View?) {
        var lblDate: TextView? = null
        var lblStart: TextView? = null
        var lblEnd: TextView? = null
        var lblBar: TextView? = null
        var lblDrinks: TextView? = null
        var lblFoods: TextView? = null
        var lblMenu: TextView? = null

        init {
            this.lblDate = row?.findViewById<TextView>(R.id.lbl_date)
            this.lblStart = row?.findViewById<TextView>(R.id.lbl_start_time)
            this.lblEnd = row?.findViewById<TextView>(R.id.lbl_end_time)
            this.lblBar = row?.findViewById<TextView>(R.id.lbl_bar_name)
            this.lblDrinks = row?.findViewById<TextView>(R.id.lbl_drinks)
            this.lblFoods = row?.findViewById<TextView>(R.id.lbl_food)
            this.lblMenu = row?.findViewById<TextView>(R.id.lbl_menu)
        }
    }
    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val view: View
        val viewHolder: ViewHolder
        if (convertView == null) {
            val inflater = activity?.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            view = inflater.inflate(R.layout.single_hh, null)
            viewHolder = ViewHolder(view)
            view.tag = viewHolder
        } else {
            view = convertView
            viewHolder = view.tag as ViewHolder
        }
        var hh = items[position]
        viewHolder.lblDate?.text = hh.hh_day
        viewHolder.lblStart?.text = hh.hh_start_time
        viewHolder.lblEnd?.text = hh.hh_end_time
        viewHolder.lblBar?.text = hh.hh_bar.bar_name
        viewHolder.lblDrinks?.text = hh.hh_drinks
        viewHolder.lblFoods?.text = hh.hh_food
        viewHolder.lblMenu?.text = hh.hh_menu

        return view as View
    }
    override fun getItem(i: Int): HH_Model {
        return items[i]
    }
    override fun getItemId(i: Int): Long {
        return i.toLong()
    }
    override fun getCount(): Int {
        return items.size
    }
}