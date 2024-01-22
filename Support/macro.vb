Sub test()
    Dim ws As Worksheet
    Set ws = Sheets("adresses") 

    Dim cht As Chart
    Set cht = ws.Shapes.AddChart2(, xlColumnClustered).Chart 

    With cht
        .SetSourceData Source:=ws.Range("A:B")
        .ApplyLayout (3) 
        .SeriesCollection(2).ApplyDataLabels
    End With
End Sub