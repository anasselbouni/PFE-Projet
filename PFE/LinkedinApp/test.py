prfl = l_m.profile_lookup(id)
        dataa = {}
        experience = []
        skills = []
        education = []
        l = [f.name for f in Linkedin_Profils._meta.get_fields()]
        for key, value in prfl.items():
            if key in l:
                dataa[key] = value
            else:
                pass

        try:
            dataa['location'] = prfl['geoLocationName'] + ' ' + prfl['geoCountryName'],
        except:
            try:
                dataa['location'] = prfl['geoLocationName'],
            except:
                try:
                    dataa['location'] = prfl['geoCountryName']
                except:
                    dataa['location'] = ''

        dataa['vanityname'] = id
        dataa['summary'] = prfl['summary']
        dataa['skills'] = prfl['skills']
        dataa['Nom'] = prfl['firstName'] + ' ' + prfl['lastName']
        dataa['Lien_Linkedin'] = 'https://www.linkedin.com/in/{}'.format(dataa['vanityname'])

        ###experience

        for i in prfl["experience"]:
            try:
                if None not in (i["timePeriod"]["startDate"]["month"],
                                i["timePeriod"]["startDate"]['year']):
                    timePeriod = ''
                if i["timePeriod"]["startDate"]['month'] is None and \
                        i["timePeriod"]["startDate"]['year'] is not None:
                    timePeriod = '{}'.format(i["timePeriod"]["startDate"]['year'])
                if i["timePeriod"]["startDate"]['month'] is not None and \
                        i["timePeriod"]["startDate"]['year'] is None:
                    timePeriod = '{}'.format(i["timePeriod"]["startDate"]['month'])
                if i["timePeriod"]["startDate"]['month'] is not None and \
                        i["timePeriod"]["startDate"]['year'] is not None:
                    timePeriod = '{}/{}'.format(i["timePeriod"]["startDate"]['month'],
                                                       i["timePeriod"]["startDate"]['year'])
            except:
                timePeriod = ''

            try:
                if i["timePeriod"]["endDate"]['month'] is None and \
                        i["timePeriod"]["endDate"]['year'] is not None:
                    timePeriod += ' - {}'.format(i["timePeriod"]["endDate"]['year'])
                if i["timePeriod"]["endDate"]['month'] is not None and \
                        i["timePeriod"]["endDate"]['year'] is not None:
                    timePeriod += ' - {}'.format(i["timePeriod"]["endDate"]['month'])
                if i["timePeriod"]["endDate"]['month'] is not None and \
                        i["timePeriod"]["endDate"]['year'] is not None:
                    timePeriod += ' - {}/{}'.format(i["timePeriod"]["endDate"]['month'],
                                                           i["timePeriod"]["endDate"]['year'])
            except:
                pass


            experience.append({
                    'PersonID': id,
                    'title': i["title"],
                    'locationName': i["locationName"],
                    'description': i["description"],
                    'companyName': i["companyName"],
                    'timePeriod': timePeriod,
                })

        ###skills
        for t in prfl["skills"]:
            skills.append(
                {
                    'PersonID': id,
                    'name': t["name"],
                }
            )

        ###education
        for i in prfl['education']:
            try:
                endate = '{}'.format(i['timePeriod']['endDate']['year'])
            except:
                endate = ''
            try:
                degreeName = i['degreeName']
            except:
                degreeName = ''
            try:
                fieldOfStudy = i['fieldOfStudy']
            except:
                fieldOfStudy = ''
            try:
                startdate = i['timePeriod']['startDate']['year']
            except:
                startdate = ''

            education.append(
                {
                    'PersonID': id,
                    'degreeName': degreeName,
                    'schoolName': i['schoolName'],
                    'fieldOfStudy': fieldOfStudy,
                    'period': '{} - {}'.format(startdate,endate),
                })