# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.propgrid as pg

###########################################################################
## Class SectionParamsDefsPanelBase
###########################################################################

class SectionParamsDefsPanelBase ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 300,919 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"截面参数定义", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"截面类型：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer4.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice_section_typeChoices = [ u"直角钢", u"工字钢", u"槽钢", u"C型钢", u"T型钢", u"帽型钢", u"J型钢" ]
		self.m_choice_section_type = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_section_typeChoices, 0 )
		self.m_choice_section_type.SetSelection( 3 )
		bSizer4.Add( self.m_choice_section_type, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"截面参数：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer6.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_grid_params_defs = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid_params_defs.CreateGrid( 7, 2 )
		self.m_grid_params_defs.EnableEditing( True )
		self.m_grid_params_defs.EnableGridLines( True )
		self.m_grid_params_defs.EnableDragGridSize( False )
		self.m_grid_params_defs.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid_params_defs.SetColSize( 0, 200 )
		self.m_grid_params_defs.EnableDragColMove( False )
		self.m_grid_params_defs.EnableDragColSize( True )
		self.m_grid_params_defs.SetColLabelSize( 30 )
		self.m_grid_params_defs.SetColLabelValue( 0, u"参数定义" )
		self.m_grid_params_defs.SetColLabelValue( 1, u"参数值" )
		self.m_grid_params_defs.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid_params_defs.EnableDragRowSize( True )
		self.m_grid_params_defs.SetRowLabelSize( 1 )
		self.m_grid_params_defs.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid_params_defs.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer6.Add( self.m_grid_params_defs, 0, wx.ALL, 5 )
		
		self.m_btn_calculation = wx.Button( self, wx.ID_ANY, u"计算", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_btn_calculation, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		self.m_panel_canvas = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,300 ), wx.TAB_TRAVERSAL )
		self.m_panel_canvas.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		
		bSizer2.Add( self.m_panel_canvas, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_propertyGrid_result = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,300 ), wx.propgrid.PG_DEFAULT_STYLE)
		self.m_propertyGridItem1 = self.m_propertyGrid_result.Append( pg.PropertyCategory( u"结果数据", u"结果数据" ) ) 
		self.m_propertyGridItem2 = self.m_propertyGrid_result.Append( pg.StringProperty( u"面积                                =", u"面积                                =" ) ) 
		self.m_propertyGridItem3 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Sx                                  =", u"Sx                                  =" ) ) 
		self.m_propertyGridItem42 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Sy                                  =", u"Sy                                  =" ) ) 
		self.m_propertyGridItem4 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Ix                                   =", u"Ix                                   =" ) ) 
		self.m_propertyGridItem5 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Iy                                   =", u"Iy                                   =" ) ) 
		self.m_propertyGridItem7 = self.m_propertyGrid_result.Append( pg.StringProperty( u"Ixy                                  =", u"Ixy                                  =" ) ) 
		self.m_propertyGridItem8 = self.m_propertyGrid_result.Append( pg.StringProperty( u"型心                                =", u"型心                                =" ) ) 
		self.m_propertyGridItem9 = self.m_propertyGrid_result.Append( pg.StringProperty( u"主惯性角                          =", u"主惯性角                          =" ) ) 
		self.m_propertyGridItem61 = self.m_propertyGrid_result.Append( pg.StringProperty( u"ix                                   =", u"ix                                   =" ) ) 
		self.m_propertyGridItem62 = self.m_propertyGrid_result.Append( pg.StringProperty( u"iy                                   =", u"iy                                   =" ) ) 
		bSizer2.Add( self.m_propertyGrid_result, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_choice_section_type.Bind( wx.EVT_CHOICE, self.OnSelectSectionType )
		self.m_btn_calculation.Bind( wx.EVT_BUTTON, self.m_btn_calculationOnButtonClick )
		self.m_btn_calculation.Bind( wx.EVT_SET_FOCUS, self.m_btn_calculationOnSetFocus )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSelectSectionType( self, event ):
		event.Skip()
	
	def m_btn_calculationOnButtonClick( self, event ):
		event.Skip()
	
	def m_btn_calculationOnSetFocus( self, event ):
		event.Skip()
	

