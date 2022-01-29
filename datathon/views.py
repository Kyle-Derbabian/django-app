from collections import defaultdict
import json

from django.shortcuts import render
from django.http import FileResponse
from datathon.forms import *
import pandas as pd

def contact(request):
    flags = []

    gender_form = GenderForm(request.POST or None)
    identity_form = IdentityForm(request.POST or None)
    religion_form = ReligionForm(request.POST or None)

    if request.method == "POST" and gender_form.is_valid() and identity_form.is_valid() and religion_form.is_valid():
        gender_selection = gender_form.cleaned_data["gender_form"]
        identity_selection = identity_form.cleaned_data["identity_form"]
        religion_selection = religion_form.cleaned_data["religion_form"]
        flags += gender_selection + identity_selection + religion_selection
        print("Flags:", flags)
        safetyMapping = run_data_stuff(flags)
        return render(request, "form.html", {"mapping": safetyMapping})
    else:
        return render(request, "form.html", {"gender_form": gender_form,
                                             "identity_form": identity_form,
                                             "religion_form": religion_form})
        






###########################################################################################

def encode_and_bind(original_dataframe, feature_to_encode):
    """
    Applies one-hot encoding to a given column of a given dataframe
    :param original_dataframe: a dataframe object
    :param feature_to_encode: the name of the column to encode
    :return: a new dataframe equivalent to original_dataframe with feature_to_encode replaced by its encoded parts
    """
    dummies = pd.get_dummies(original_dataframe[[feature_to_encode]])
    res = pd.concat([original_dataframe, dummies], axis=1)
    res.drop(columns=[feature_to_encode], inplace=True)
    return res


def run_data_stuff(flags):
    
    PRECINCT_LOCATIONS = {
        1: (40.720290149107775, -74.00706752420079),
        5: (40.71616206837045, -73.99736097878551),
        6: (40.73433145218006, -74.00548984819274),
        7: (40.71642625379399, -73.98391177328836),
        9: (40.72643962639678, -73.98789896000012),
        10: (40.74269248038469, -73.99865632194924),
        13: (40.7368708183241, -73.98286408688828),
        14: (40.75388112931714, -73.99494463938726),
        17: (40.75681236059047, -73.97075782184231),
        18: (40.76497726651173, -73.98512230416158),
        19: (40.76713270451236, -73.96378311823159),
        20: (40.78406154787142, -73.9749844832864),
        22: (40.783725319901, -73.9655548025621),
        23: (40.7890864686238, -73.9470372055556),
        24: (40.796492015116826, -73.96727748466826),
        25: (40.80076135424946, -73.94108180256144),
        26: (40.81474570769272, -73.9563714610815),
        28: (40.808827663410526, -73.95256235617789),
        30: (40.82871328082459, -73.94364879423992),
        32: (40.815774827868594, -73.94533951926367),
        34: (40.84069823105439, -73.9357356752305),
        40: (40.81035256819006, -73.92520432458674),
        41: (40.81626366262125, -73.89564198132042),
        42: (40.82248136629819, -73.9112712035922),
        43: (40.82303519278026, -73.8698255650016),
        44: (40.83738313410182, -73.91964806671724),
        45: (40.83084050884495, -73.8273204416355),
        46: (40.85396264400858, -73.90011185008728),
        47: (40.88746629399387, -73.8475471878505),
        48: (40.84386441287738, -73.90045114351796),
        49: (40.856105207687214, -73.84445994064775),
        50: (40.88355502406457, -73.90237481039455),
        52: (40.86908012475324, -73.87968233884756),
        60: (40.57656953753706, -73.97619017554969),
        61: (40.59414150295453, -73.96050168353948),
        62: (40.60254509071344, -74.00313005483962),
        63: (40.62796800454618, -73.94163314790221),
        66: (40.625737408230684, -73.99143554684944),
        67: (40.64864013485931, -73.95024781346117),
        68: (40.638975527571844, -74.02265510352635),
        70: (40.63038253207545, -73.97375440464934),
        71: (40.664574602155625, -73.94784550050991),
        72: (40.65830755108979, -74.00087399541049),
        73: (40.67088021121846, -73.91353335402417),
        75: (40.6712428927309, -73.8815381195398),
        76: (40.68381082021514, -74.00024004173127),
        77: (40.674605291128415, -73.930241720314),
        78: (40.67537249490615, -73.99426086387884),
        79: (40.688821952013406, -73.9447413310038),
        81: (40.689659588455456, -73.92445191347043),
        83: (40.69825775478788, -73.91785034143308),
        84: (40.695653789712644, -73.98289217854035),
        88: (40.690033079537244, -73.96051489480203),
        90: (40.70635441300016, -73.95078220112747),
        94: (40.7267261163633, -73.95330617594506)
    }
    
    print("==================================================")
    
    df = pd.read_csv("datathon/NYPD_Hate_Crimes.csv")
    df.reset_index(inplace=True)
    df.drop(columns=["index", "Full Complaint ID", "Complaint Year Number", "Month Number", "Record Create Date", "Patrol Borough Name", "Law Code Category Description", "Offense Description", "PD Code Description", "Arrest Date", "Arrest Id"], inplace=True)
    df = encode_and_bind(df, "Bias Motive Description")
    df.rename(columns={"Complaint Precinct Code": "Precinct"}, inplace=True)
    df.drop(columns="Bias Motive Description_60 YRS AND OLDER", inplace=True)
    df.rename(columns={
                       "Bias Motive Description_ANTI-ARAB": "Arab",
                       "Bias Motive Description_ANTI-ASIAN": "Asian",
                       "Bias Motive Description_ANTI-BLACK": "Black",
                       "Bias Motive Description_ANTI-BUDDHIST": "Buddhist",
                       "Bias Motive Description_ANTI-CATHOLIC": "Catholic",
                       "Bias Motive Description_ANTI-FEMALE": "Female",
                       "Bias Motive Description_ANTI-FEMALE HOMOSEXUAL (LESBIAN)": "Lesbian",
                       "Bias Motive Description_ANTI-GENDER NON-CONFORMING": "Non-Conforming",
                       "Bias Motive Description_ANTI-HINDU": "Hindu",
                       "Bias Motive Description_ANTI-HISPANIC": "Hispanic",
                       "Bias Motive Description_ANTI-JEHOVAHS WITNESS": "Jehovah's Witness",
                       "Bias Motive Description_ANTI-JEWISH": "Jewish",
                       "Bias Motive Description_ANTI-LGBT (MIXED GROUP)": "LGBT",
                       "Bias Motive Description_ANTI-MALE HOMOSEXUAL (GAY)": "Gay",
                       "Bias Motive Description_ANTI-MULTI-RACIAL GROUPS": "Multiracial",
                       "Bias Motive Description_ANTI-MUSLIM": "Muslim",
                       "Bias Motive Description_ANTI-OTHER ETHNICITY": "Other Ethnicity",
                       "Bias Motive Description_ANTI-OTHER RELIGION": "Other Religion",
                       "Bias Motive Description_ANTI-PHYSICAL DISABILITY": "Physical Disability",
                       "Bias Motive Description_ANTI-RELIGIOUS PRACTICE GENERALLY": "Religious",
                       "Bias Motive Description_ANTI-TRANSGENDER": "Transgender",
                       "Bias Motive Description_ANTI-WHITE": "White"
                       }, inplace=True)
    
    precincts = list(set(df["Precinct"]))
    precincts.sort()
    
    precinct_safety = {}
    for precinct_number, precinct_coordinates in PRECINCT_LOCATIONS.items():
        precinct_subset = df[df["Precinct"] == precinct_number]
        precinct_total = len(precinct_subset)
        
        counts = defaultdict(int)
        for flag in flags:
            if (flag in df.columns):
                for binary in precinct_subset[flag]:
                    if binary == 1:
                        counts[flag] += 1
        flags_total = sum(dict(counts).values())
        safety_score = (precinct_total - flags_total) / precinct_total
        danger_score = flags_total / precinct_total
        precinct_safety[precinct_coordinates] = danger_score
        
        print(dict(counts))
        print("Precinct", precinct_number, precinct_coordinates, "total crime:", precinct_total)
        print("Precinct", precinct_coordinates, "flagged crime:", flags_total)
        print("Precinct", precinct_coordinates, "danger score:", danger_score)
        print()
    
    # print(precinct_safety)
    
    return precinct_safety
    # return render(request, "form.html", {"coordinatesToSafetyMapping": precinct_safety})
    