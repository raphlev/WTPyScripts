Attribute VB_Name = "Module1"
'''
The Main subroutine orchestrates the execution of multiple tasks:
- Calls ListTCISColumnHeaders: Processes TCIS column headers
- Calls ListWINDCHILLColumnHeaders: Processes Windchill column headers
- Calls ListTCISAttributesCount: Counts non-null values for TCIS attributes
- Displays a message box once all functions complete successfully
'''
Sub Main()
    ' Call the first function processing TCIS column headers
    Call ListTCISColumnHeaders
    ' Call the second function processing WINDCHILL column headers
    Call ListWINDCHILLColumnHeaders
    ' Call the third function processing TCIS Count of usage
    Call ListTCISAttributesCount

    MsgBox "Processes to calculate Windchill Attributes and TCIS Attributes and TCIS attributes usage count completed successfully!", vbInformation
End Sub


'''
ListTCISColumnHeaders
This function processes TCIS column headers:
- Inputs: column D of 'Matrice_WindchillTCIS'
- Outputs: column E
- Searches headers between columns AP and AEO1 in 'Merged_TCIS'
- Finds non-null values associated with input headers
- Populates output cells with unique headers as a list
'''
Sub ListTCISColumnHeaders()
    Dim wsInput As Worksheet, wsLookup As Worksheet
    Dim dataArray As Variant, headerArray As Variant
    Dim cell As Variant, headerCell As Range
    Dim lookupFirstRow As Long, lookupLastRow As Long
    Dim result As String
    Dim colStart As Long, colEnd As Long
    Dim colIndex As Long, inputRow As Long
    Dim inputFirstRow As Long, inputLastRow As Long
    Dim dict As Object
    Dim i As Long

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    Set dict = CreateObject("Scripting.Dictionary")
    ' Set the worksheets
    Set wsInput = ThisWorkbook.Sheets("Matrice_WindchillTCIS")
    Set wsLookup = ThisWorkbook.Sheets("Merged_TCIS")

    ' Clear existing filters on the lookup worksheet
    If wsLookup.AutoFilterMode Then
        wsLookup.AutoFilterMode = False
    End If
    
    ' Define input rows range using last non-empty row in column D
    inputFirstRow = 2
    inputLastRow = wsInput.Cells(wsInput.Rows.Count, "D").End(xlUp).Row

    ' Define the range to search the value in column 'AJ' using the last non-empty row
    lookupFirstRow = 2
    lookupLastRow = wsLookup.Cells(wsLookup.Rows.Count, "AJ").End(xlUp).Row
    dataArray = wsLookup.Range("AJ" & lookupFirstRow & ":AJ" & lookupLastRow).Value ' Load the range into an array for faster processing

    ' Define the start and end columns by their headers from AP1 to AEO1
    colStart = wsLookup.Range("AP1").Column
    colEnd = wsLookup.Range("AEO1").Column
    headerArray = wsLookup.Range(wsLookup.Cells(1, colStart), wsLookup.Cells(1, colEnd)).Value ' Load header names into an array

    ' Process each input value from column D
    For inputRow = inputFirstRow To inputLastRow
        dict.RemoveAll  ' Clear the dictionary for each new input row
        result = ""  ' Clear previous results
        
        ' Search for the value in column D of the current inputRow across the specified range in 'AJ'
        For i = 1 To UBound(dataArray, 1)
            If Trim(CStr(dataArray(i, 1))) = Trim(CStr(wsInput.Cells(inputRow, "D").Value)) Then
                ' Check columns from 'AP' to 'AEO1'
                For colIndex = colStart To colEnd
                    If Not IsEmpty(wsLookup.Cells(i + lookupFirstRow - 1, colIndex).Value) Then
                        ' Get the header from the first row array
                        If Not dict.Exists(headerArray(1, colIndex - colStart + 1)) Then
                            dict.Add headerArray(1, colIndex - colStart + 1), Nothing
                        End If
                    End If
                Next colIndex
            End If
        Next i

        ' Combine all headers in the dictionary into one string
        For Each Key In dict.Keys
            result = result & Key & vbCrLf
        Next
        
        ' Remove the last carriage return
        If Len(result) > 0 Then
            result = Left(result, Len(result) - 1)
        End If
        
        ' Output the result in corresponding row 'E' column
        wsInput.Cells(inputRow, "E").Value = result
    Next inputRow
    
    Application.EnableEvents = True
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True

    Exit Sub

End Sub


'''
ListWINDCHILLColumnHeaders
This function processes Windchill column headers:
- Inputs: column B of 'Matrice_WindchillTCIS'
- Outputs: column A
- Searches attributes names in column H in 'Windchill Classif Nodes+Attr'

- Finds non-null values associated with input headers
- Populates output cells with unique headers as a list
'''
Sub ListWINDCHILLColumnHeaders()
    Dim wsInput As Worksheet, wsLookup As Worksheet
    Dim dataArray As Variant, resultArray As Variant
    Dim inputFirstRow As Long, inputLastRow As Long
    Dim result As String
    Dim colIndex As Long, inputRow As Long
    Dim dict As Object
    Dim i As Long

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    Set dict = CreateObject("Scripting.Dictionary")
    ' Set the worksheets
    Set wsInput = ThisWorkbook.Sheets("Matrice_WindchillTCIS")
    Set wsLookup = ThisWorkbook.Sheets("Windchill Classif Nodes+Attr")
    
    ' Clear existing filters on the lookup worksheet
    If wsLookup.AutoFilterMode Then
        wsLookup.AutoFilterMode = False
    End If

    ' Define input rows range using last non-empty row in column B
    inputFirstRow = 2
    inputLastRow = wsInput.Cells(wsInput.Rows.Count, "B").End(xlUp).Row

    ' Load input values from column C and H in Windchill sheet
    dataArray = wsLookup.Range("C2:C" & wsLookup.Cells(wsLookup.Rows.Count, "C").End(xlUp).Row).Value
    resultArray = wsLookup.Range("H2:H" & wsLookup.Cells(wsLookup.Rows.Count, "H").End(xlUp).Row).Value

    ' Process each input value from column B
    For inputRow = inputFirstRow To inputLastRow
        dict.RemoveAll ' Clear the dictionary for each new input row
        result = "" ' Clear previous results

        ' Search in the lookup array
        For i = 1 To UBound(dataArray, 1)
            If Trim(CStr(dataArray(i, 1))) = Trim(CStr(wsInput.Cells(inputRow, "B").Value)) Then
                cellValue = Trim(CStr(resultArray(i, 1)))
                If cellValue <> "" Then
                    If Not dict.Exists(cellValue) Then
                        dict.Add cellValue, Nothing
                    End If
                End If
            End If
        Next i

        ' Combine all valid headers into one string separated by carriage returns
        For Each Key In dict.Keys
            result = result & Key & vbCrLf
        Next

        ' Remove the last carriage return
        If Len(result) > 0 Then
            result = Left(result, Len(result) - 1)
        End If

        ' Output the result into column A of the current row in wsInput
        wsInput.Cells(inputRow, "A").Value = result
    Next inputRow

    Application.EnableEvents = True
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True

End Sub

'''
ListTCISAttributesCount
This function counts non-null values for TCIS attributes:
- Inputs: column B of 'NbUsageTCIS'
- Outputs: column C
- Counts non-null values for each header between columns AP and AEO1 in 'Merged_TCIS'
- Populates output cells with the count of non-null values
'''
Sub ListTCISAttributesCount()
    Dim wsInput As Worksheet, wsLookup As Worksheet
    Dim inputRow As Long, inputFirstRow As Long, inputLastRow As Long
    Dim colStart As Long, colEnd As Long
    Dim headerRow As Range, header As String
    Dim countNonNull As Long
    Dim headerCell As Range
    Dim rowIndex As Long, colIndex As Long

    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    ' Set the worksheets
    Set wsInput = ThisWorkbook.Sheets("NbUsageTCIS")
    Set wsLookup = ThisWorkbook.Sheets("Merged_TCIS")

    ' Clear existing filters on the lookup worksheet
    If wsLookup.AutoFilterMode Then
        wsLookup.AutoFilterMode = False
    End If

    ' Define the input range
    inputFirstRow = 2
    inputLastRow = wsInput.Cells(wsInput.Rows.Count, "B").End(xlUp).Row

    ' Define the columns to search in 'Merged_TCIS' from AP1 to AEO1
    colStart = wsLookup.Range("AP1").Column
    colEnd = wsLookup.Range("AEO1").Column

    ' Loop through each input row in NbUsageTCIS from column B
    For inputRow = inputFirstRow To inputLastRow
        countNonNull = 0 ' Reset the count

        ' Get the header name from column B
        header = Trim(CStr(wsInput.Cells(inputRow, "B").Value))

        ' Find the header in 'Merged_TCIS'
        Set headerRow = wsLookup.Rows(1)

        Set headerCell = Nothing
        For colIndex = colStart To colEnd
            If Trim(CStr(headerRow.Cells(1, colIndex).Value)) = header Then
                Set headerCell = headerRow.Cells(1, colIndex)
                Exit For
            End If
        Next colIndex

        ' If headerCell is found, count non-null and non-empty values in the column
        If Not headerCell Is Nothing Then
            For rowIndex = 2 To wsLookup.Cells(wsLookup.Rows.Count, headerCell.Column).End(xlUp).Row
                If Trim(CStr(wsLookup.Cells(rowIndex, headerCell.Column).Value)) <> "" Then
                    countNonNull = countNonNull + 1
                End If
            Next rowIndex
        End If

        ' Output the count in column C
        wsInput.Cells(inputRow, "C").Value = countNonNull
    Next inputRow

    Application.EnableEvents = True
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True

End Sub
