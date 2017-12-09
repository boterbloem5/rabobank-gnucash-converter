import csv



# As described in https://www.rabobank.nl/images/formaatbeschrijving_csv_kommagescheiden_nieuw_29539176.pdf
csv_fieldnames = [
    "account", #REKENINGNUMMER_REKENINGHOUDER
    "currency", #MUNTSOORT
    "interest_date", #RENTEDATUM
    "transaction_class", #BY_AF_CODE
    "amount", #BEDRAG
    "contra_account", #TEGENREKENING
    "to_name", #NAAR_NAAM
    "transaction_date", #BOEKDATUM
    "transaction_type", #BOEKCODE
    "", #FILLER
    "description1", #OMSCHR1
    "description2", #OMSCHR2
    "description3", #OMSCHR3
    "description4", #OMSCHR4
    "description5", #OMSCHR5
    "description6", #OMSCHR6
    "SEPA_ID", #END_TO_END_ID
    "SEPA_contra", #ID_TEGENREKENINGHOUDER
    "SEPA_mandate" #MANDAAT_ID
    ]

def importer(filename):

    """
    Import .csv file with transaction data
    """

    transaction_data = open(filename )

    transaction_dict = csv.DictReader(transaction_data, fieldnames=csv_fieldnames)

    return transaction_dict

def qif_writer(transaction_dict):
    """
    """



    writestring = """
D{transaction_date}
T{amount}
P{contra_account} {to_name} {description}
^

        """.format(**transaction_dict)

    return writestring


def qif_return(filename):

    with open('static/transactions.qif', 'w' ) as outfile:
        outfile.write("!Type:Bank")
        outfile.write("\n\n")

        for transaction in importer(filename):

            if transaction["transaction_class"] == "D": #debet
                transaction["amount"] = "-" + transaction["amount"]

            transaction["description"] = " ".join([transaction["description1"],
                                        transaction["description2"],
                                        transaction["description3"],
                                        transaction["description4"],
                                        transaction["description5"],
                                        transaction["description6"]]).strip()

            writestring = qif_writer(transaction)
            outfile.write(writestring)




if __name__ == '__main__':
    importer("transactions.txt")

    with open('output.qif', 'w' ) as outfile:
        outfile.write("!Type:Bank")
        outfile.write("\n\n")

        for transaction in importer("transactions.txt"):

            if transaction["transaction_class"] == "D": #debet
                transaction["amount"] = "-" + transaction["amount"]

            transaction["description"] = " ".join([transaction["description1"],
                                        transaction["description2"],
                                        transaction["description3"],
                                        transaction["description4"],
                                        transaction["description5"],
                                        transaction["description6"]]).strip().strip()

            writestring = qif_writer(transaction)
            outfile.write(writestring)

