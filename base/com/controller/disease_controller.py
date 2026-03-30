from flask import render_template, request, redirect
from base import app
from base.com.dao.crop_dao import CropDAO
from base.com.vo.disease_vo import DiseaseVO
from base.com.dao.disease_dao import DiseaseDAO


@app.route('/viewDisease')
def viewDisease():
    try:
        disease_dao = DiseaseDAO()
        disease_list = disease_dao.view_disease()

        return render_template("admin/viewDisease.html", disease_list=disease_list)

    except Exception as e:
        print("ERROR in viewDisease:", e)
        return render_template("admin/viewDisease.html",disease_list=[])





@app.route('/addDisease',methods=['GET', 'POST'])
def addDisease():
    try:
        crop_dao = CropDAO()
        crop_list = crop_dao.view_all_crops()
        crop_vo_list = [i.as_dict() for i in crop_list]

        return render_template("admin/addDisease.html", crop_vo_list=crop_vo_list)

    except Exception as e:
        print("ERROR in addDisease:",e)
        return render_template("admin/addDisease.html",crop_vo_list=[])


@app.route('/insertDisease', methods=["POST"])
def insertDisease():
    try:
        disease_name = request.form.get('disease_name')
        disease_description = request.form.get('disease_description')
        disease_crop_id = request.form.get('disease_crop_id')

        disease_vo = DiseaseVO()
        disease_vo.disease_name = disease_name
        disease_vo.disease_description = disease_description
        disease_vo.disease_crop_id = disease_crop_id

        disease_dao = DiseaseDAO()
        disease_dao.insert_disease(disease_vo)

        return redirect('/viewDisease')

    except Exception as e:
        print("ERROR IN insertDisease",e)
        return redirect('/addDisease')




@app.route('/editDisease')
def editDisease():
    try:
        disease_id = request.args.get('disease_id')

        disease_dao = DiseaseDAO()
        disease_vo = disease_dao.edit_disease(disease_id)

        crop_dao = CropDAO()
        crop_list = crop_dao.view_all_crops()
        crop_vo_list = [i.as_dict() for i in crop_list]

        return render_template(
            "admin/editDisease.html",disease=disease_vo,crop_vo_list=crop_vo_list )

    except Exception as e:
        print("Error in editDisease",e)
        return render_template("admin/editDisease.html", disease=[], crop_vo_list=[])




# ADDED: Handle the update form submission
@app.route('/updateDisease', methods=["POST"])
def updateDisease():
    try:
        disease_id = request.form.get('disease_id')
        disease_name = request.form.get('disease_name')
        disease_description = request.form.get('disease_description')
        disease_crop_id = request.form.get('disease_crop_id')

        disease_vo = DiseaseVO()
        disease_vo.disease_id = disease_id
        disease_vo.disease_name = disease_name
        disease_vo.disease_description = disease_description
        disease_vo.disease_crop_id = disease_crop_id

        disease_dao = DiseaseDAO()
        disease_dao.update_disease(disease_vo)

        return redirect('/viewDisease')
    except Exception as e:
        print("error in updateDisease",e)
        return redirect("/viewDisease")


@app.route('/deleteDisease')
def deleteDisease():
    try:
        disease_id = request.args.get('disease_id')

        disease_dao = DiseaseDAO()
        disease_dao.delete_disease(disease_id)

        return redirect('/viewDisease')
    except Exception as e:
        print("error in deleteDisease",e)
        return redirect('/viewDisease')