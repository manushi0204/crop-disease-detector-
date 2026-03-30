from flask import render_template, request, redirect
from base import app
from base.com.dao.crop_dao import CropDAO
from base.com.vo.crop_vo import CropVO



@app.route('/addCrops', methods=['GET', 'POST'])
def addCrops():
        try:
            if request.method == 'POST':
                crop_name = request.form.get('crop_name')
                crop_description = request.form.get('crop_description')

                crop_vo = CropVO()
                crop_vo.crop_name = crop_name
                crop_vo.crop_description = crop_description

                crop_dao = CropDAO()
                crop_dao.insert_crop(crop_vo)

                return redirect('/viewCrops')
                return render_template("admin/addCrops.html")

        except Exception as e:
            print("ERROR in addCrops:", e)
            return redirect('/addCrops')




@app.route('/viewCrops')
def viewCrops():
    try:
        crop_dao = CropDAO()
        crop_list = crop_dao.view_all_crops()
        crop_vo_list=[i.as_dict() for i in crop_list]
        return render_template("admin/viewCrop.html",crop_vo_list=crop_vo_list)

    except Exception as e:
        print("ERROR in viewCrops:", e)
        return render_template("admin/viewCrop.html",crop_vo_list=[])


@app.route('/editCrops', methods=['GET', 'POST'])
def editCrops():

    crop_dao = CropDAO()
    try:#post-update
        if request.method == 'POST':
            crop_vo = CropVO()
            crop_vo.crop_id = int(request.form.get('crop_id'))
            crop_vo.crop_name = request.form.get('crop_name')
            crop_vo.crop_description = request.form.get('crop_description')

            crop_dao.update_crop(crop_vo)
            return redirect('/viewCrops')
        #get-load
        crop_id = int(request.args.get('crop_id'))
        crop = crop_dao.get_by_id(crop_id)

        return render_template("admin/editCrop.html", crop=crop)

    except Exception as e:
        print("ERROR in editCrops:", e)
        return redirect('/viewCrops')


@app.route('/deleteCrops')
def deleteCrops():
    try:
        crop_id = int(request.args.get('crop_id'))

        crop_vo = CropVO()
        crop_vo.crop_id = crop_id

        crop_dao = CropDAO()
        crop_dao.delete_crop(crop_vo)

        return redirect('/viewCrops')

    except Exception as e:
        print("ERROR in deleteCrops:", e)
        return redirect('/viewCrops')

